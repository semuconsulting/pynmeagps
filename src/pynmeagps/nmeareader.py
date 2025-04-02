"""
NMEAReader class.

Reads and parses individual NMEA GNSS/GPS messages from
any stream which supports a read(n) -> bytes method.

Can also read from socket via SocketStream wrapper.

Returns both the raw binary data (as bytes) and the parsed
data (as an NMEAMessage object).

Implements an iterator: `for raw, parsed in NMEAReader(stream):`

If the 'nmeaonly' kwarg is set to 'True', the reader
will raise a NMEAParseError if it encounters any non-NMEA
data. Otherwise, it will ignore the non-NMEA data and attempt
to carry on.

Created on 4 Mar 2021

:author: semuadmin
:copyright: SEMU Consulting © 2021
:license: BSD 3-Clause
"""

# pylint: disable=too-many-positional-arguments

from logging import getLogger
from socket import socket

import pynmeagps.exceptions as nme
from pynmeagps.nmeahelpers import calc_checksum, get_parts
from pynmeagps.nmeamessage import NMEAMessage
from pynmeagps.nmeatypes_core import (
    ERR_LOG,
    ERR_RAISE,
    GET,
    NMEA_HDR,
    VALCKSUM,
    VALMSGID,
)
from pynmeagps.socketwrapper import SocketWrapper


class NMEAReader:
    """
    NMEAReader class.
    """

    def __init__(
        self,
        stream,
        msgmode: int = GET,
        validate: int = VALCKSUM,
        nmeaonly: bool = False,
        quitonerror: int = ERR_LOG,
        bufsize: int = 4096,
        errorhandler: object = None,
        userdefined: dict = None,
    ):
        """Constructor.

        :param stream stream: input data stream (e.g. Serial or binary File)
        :param int msgmode: 0=GET, 1=SET, 2=POLL (0)
        :param int validate: VALNONE (0), VALCKSUM (1), VALMSGID (2),
            (can be OR'd) (1)
        :param bool nmeaonly: True = error on non-NMEA data, False = ignore non-NMEA data
        :param int quitonerror: ERR_IGNORE (0) = ignore errors,  ERR_LOG (1) = log continue,
            ERR_RAISE (2) = (re)raise (1)
        :param int bufsize: socket recv buffer size (4096)
        :param object errorhandler: error handling object or function (None)
        :param dict userdefined: user-defined payload definition dictionary (None)
        :raises: NMEAParseError (if mode is invalid)
        """
        # pylint: disable=too-many-arguments

        if isinstance(stream, socket):
            self._stream = SocketWrapper(stream, bufsize=bufsize)
        else:
            self._stream = stream
        if msgmode not in (0, 1, 2):
            raise nme.NMEAParseError(
                f"Invalid stream mode {msgmode} - must be 0, 1 or 2."
            )
        self._quitonerror = quitonerror
        self._errorhandler = errorhandler
        self._nmea_only = nmeaonly
        self._validate = validate
        self._mode = msgmode
        self._userdefined = userdefined
        self._logger = getLogger(__name__)

    def __iter__(self):
        """Iterator."""

        return self

    def __next__(self) -> tuple:
        """
        Return next item in iteration.

        :return: tuple of (raw_data as bytes, parsed_data as NMEAMessage)
        :rtype: tuple
        :raises: StopIteration

        """

        (raw_data, parsed_data) = self.read()
        if raw_data is None and parsed_data is None:
            raise StopIteration
        return (raw_data, parsed_data)

    def read(self) -> tuple:
        """
        Read the binary data from the stream buffer.

        :return: tuple of (raw_data as bytes, parsed_data as NMEAMessage)
        :rtype: tuple
        :raises: NMEAStreamError (if nmeaonly=True and stream includes non-NMEA data)

        """

        parsing = True
        raw_data = None
        parsed_data = None

        while parsing:  # loop until end of valid NMEA message or EOF
            try:
                byte1 = self._read_bytes(1)  # read 1st byte
                if byte1 != b"\x24":  # not NMEA, discard and continue
                    continue
                byte2 = self._read_bytes(1)  # read 2nd byte to confirm protocol
                bytehdr = byte1 + byte2
                if bytehdr in NMEA_HDR:  # it's a NMEA message
                    byten = self._read_line()  # NMEA protocol is CRLF terminated
                    raw_data = bytehdr + byten
                    parsed_data = self.parse(
                        raw_data,
                        msgmode=self._mode,
                        validate=self._validate,
                        userdefined=self._userdefined,
                    )
                    parsing = False
                else:  # it's not a NMEA message (UBX or something else)
                    if self._nmea_only:  # raise error and quit
                        raise nme.NMEAParseError(f"Unknown protocol header {bytehdr}.")

            except EOFError:
                return (None, None)
            except (
                nme.NMEAMessageError,
                nme.NMEATypeError,
                nme.NMEAParseError,
                nme.NMEAStreamError,
            ) as err:
                if self._quitonerror:
                    self._do_error(err)
                continue

        return (raw_data, parsed_data)

    def _read_bytes(self, size: int) -> bytes:
        """
        Read a specified number of bytes from stream.

        :param int size: number of bytes to read
        :return: bytes
        :rtype: bytes
        :raises: EOFError if stream ends prematurely
        """

        data = self._stream.read(size)
        if len(data) == 0:  # EOF
            raise EOFError()  # pragma: no cover
        if 0 < len(data) < size:  # truncated stream
            raise nme.NMEAStreamError(  # pragma: no cover
                "Serial stream terminated unexpectedly. "
                f"{size} bytes requested, {len(data)} bytes returned."
            )
        return data

    def _read_line(self) -> bytes:
        """
        Read bytes until LF (0x0a) terminator.

        :return: bytes
        :rtype: bytes
        :raises: EOFError if stream ends prematurely
        """

        data = self._stream.readline()  # NMEA protocol is CRLF-terminated
        if len(data) == 0:  # EOF
            raise EOFError()  # pragma: no cover
        if data[-1:] != b"\x0a":  # truncated stream
            raise nme.NMEAStreamError(  # pragma: no cover
                "Serial stream terminated unexpectedly. "
                f"Line requested, {len(data)} bytes returned."
            )
        return data

    def _do_error(self, err: Exception):
        """
        Handle error.

        :param Exception err: error message
        :raises: Exception if quitonerror = 2
        """

        if self._quitonerror == ERR_RAISE:
            raise err from err
        if self._quitonerror == ERR_LOG:
            # pass to error handler if there is one
            if self._errorhandler is None:
                self._logger.error(err)
            else:
                self._errorhandler(err)

    @property
    def datastream(self) -> object:
        """
        Getter for stream.

        :return: data stream
        :rtype: object
        """

        return self._stream

    @staticmethod
    def parse(
        message: bytes,
        msgmode: int = GET,
        validate: int = VALCKSUM,
        userdefined: dict = None,
    ) -> object:
        """
        Parse NMEA byte stream to NMEAMessage object.

        :param bytes message: bytes message to parse
        :param int msgmode: 0=GET, 1=SET, 2=POLL (0)
        :param int validate: VALNONE (0), VALCKSUM (1), VALMSGID (2),
            (can be OR'd) (1)
        :param dict userdefined: user-defined payload definition dictionary (None)
        :return: NMEAMessage object (or None if unknown message and VALMSGID is not set)
        :rtype: NMEAMessage
        :raises: NMEAParseError (if data stream contains invalid data or unknown message type)

        """

        if msgmode not in (0, 1, 2):
            raise nme.NMEAParseError(
                f"Invalid parse mode {msgmode} - must be 0, 1 or 2."
            )

        try:
            content, talker, msgid, payload, checksum = get_parts(message)
            if validate & VALCKSUM:
                ccksum = calc_checksum(content)
                if checksum.upper() != ccksum:
                    raise nme.NMEAParseError(
                        f"Message {talker}{msgid} invalid checksum {checksum}"
                        f" - should be {ccksum}."
                    )
            return NMEAMessage(
                talker,
                msgid,
                msgmode,
                payload=payload,
                checksum=checksum,
                validate=validate,
                userdefined=userdefined,
            )

        except nme.NMEAMessageError as err:
            if validate & VALMSGID:
                raise nme.NMEAParseError(err)
            return None
