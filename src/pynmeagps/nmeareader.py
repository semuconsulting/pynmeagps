"""
NMEAReader class.

Reads and parses individual NMEA GNSS/GPS messages from
any stream which supports a read(n) -> bytes method.

Can also read from socket via SocketStream wrapper.

Returns both the raw binary data (as bytes) and the parsed
data (as a NMEAMessage object).

If the 'nmeaonly' kwarg is set to 'True', the reader
will raise a NMEAParseError if it encounters any non-NMEA
data. Otherwise, it will ignore the non-NMEA data and attempt
to carry on.

Created on 4 Mar 2021

:author: semuadmin
:copyright: SEMU Consulting © 2021
:license: BSD 3-Clause
"""

from socket import socket
from pynmeagps.socket_stream import SocketStream
from pynmeagps.nmeamessage import NMEAMessage
import pynmeagps.exceptions as nme
from pynmeagps.nmeahelpers import (
    get_parts,
    calc_checksum,
    isvalid_cksum,
)
from pynmeagps.nmeatypes_core import (
    NMEA_HDR,
    VALCKSUM,
    VALMSGID,
    ERR_LOG,
    ERR_RAISE,
)


class NMEAReader:
    """
    NMEAReader class.
    """

    def __init__(self, stream, **kwargs):
        """Constructor.

        :param stream stream: input data stream (e.g. Serial or binary File)
        :param int quitonerror: (kwarg) 0 = ignore errors, 1 = log errors and continue, 2 = (re)raise errors (1)
        :param int errorhandler: (kwarg) error handling object or function (None)
        :param bool nmeaonly (kwarg): True = error on non-NMEA data, False = ignore non-NMEA data
        :param int validate (kwarg): bitfield validation flags - VALCKSUM (default), VALMSGID
        :param int msgmode (kwarg): 0 = GET (default), 1 = SET, 2 = POLL
        :param int bufsize: (kwarg) socket recv buffer size (4096)
        :raises: NMEAParseError (if mode is invalid)

        """

        bufsize = int(kwargs.get("bufsize", 4096))
        if isinstance(stream, socket):
            self._stream = SocketStream(stream, bufsize=bufsize)
        else:
            self._stream = stream
        nmeaonly = kwargs.get("nmeaonly", False)
        validate = kwargs.get("validate", VALCKSUM)
        msgmode = kwargs.get("msgmode", 0)
        if msgmode not in (0, 1, 2):
            raise nme.NMEAParseError(
                f"Invalid stream mode {msgmode} - must be 0, 1 or 2."
            )
        self._quitonerror = kwargs.get("quitonerror", ERR_LOG)
        self._errorhandler = kwargs.get("errorhandler", None)
        self._nmea_only = nmeaonly
        self._validate = validate
        self._mode = msgmode

    def __iter__(self):
        """Iterator."""

        return self

    def __next__(self) -> (bytes, NMEAMessage):
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

    def read(self) -> (bytes, NMEAMessage):
        """
        Read the binary data from the stream buffer.

        :return: tuple of (raw_data as bytes, parsed_data as NMEAMessage)
        :rtype: tuple
        :raises: NMEAStreamError (if nmeaonly=True and stream includes non-NMEA data)

        """

        parsing = True
        raw_data = None
        parsed_data = None

        try:
            while parsing:  # loop until end of valid NMEA message or EOF
                byte1 = self._read_bytes(1)  # read 1st byte
                if byte1 != b"\x24":  # not NMEA, discard and continue
                    continue
                byte2 = self._read_bytes(1)  # read 2nd byte to confirm protocol
                bytehdr = byte1 + byte2
                if bytehdr in NMEA_HDR:  # it's a NMEA message
                    byten = self._read_line()  # NMEA protocol is CRLF terminated
                    raw_data = bytehdr + byten
                    parsed_data = self.parse(
                        raw_data, validate=self._validate, msgmode=self._mode
                    )
                    parsing = False
                else:  # it's not a NMEA message (UBX or something else)
                    if self._nmea_only:  # raise error and quit
                        raise nme.NMEAParseError(f"Unknown data header {bytehdr}.")

        except EOFError:
            return (None, None)
        except (
            nme.NMEAMessageError,
            nme.NMEATypeError,
            nme.NMEAParseError,
            nme.NMEAStreamError,
        ) as err:
            if self._quitonerror:
                self._do_error(str(err))
            parsed_data = str(err)

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
        if len(data) < size:  # EOF
            raise EOFError()
        return data

    def _read_line(self) -> bytes:
        """
        Read until end of line (CRLF).

        :return: bytes
        :rtype: bytes
        :raises: EOFError if stream ends prematurely
        """

        data = self._stream.readline()  # NMEA protocol is CRLF terminated
        if data[-2:] != b"\x0d\x0a":  # EOF
            raise EOFError()
        return data

    def _do_error(self, err: str):
        """
        Handle error.

        :param str err: error message
        :raises: UBXParseError if quitonerror = 2
        """

        if self._quitonerror == ERR_RAISE:
            raise nme.NMEAParseError(err)
        if self._quitonerror == ERR_LOG:
            # pass to error handler if there is one
            if self._errorhandler is None:
                print(err)
            else:
                self._errorhandler(err)

    def iterate(self, **kwargs) -> tuple:  # pylint: disable=unused-argument
        """
        DEPRECATED - WILL BE REMOVED IN VERSION >=1.2.21
        USE STANDARD ITERATOR INSTEAD
        Invoke the iterator within an exception handling framework.

        :return: tuple of (raw_data as bytes, parsed_data as NMEAMessage)
        :rtype: tuple
        :raises: NMEA...Error (if quitonerror is True and stream is invalid)
        """

        while True:
            try:
                yield next(self)
            except StopIteration:
                break

    @staticmethod
    def parse(message: bytes, **kwargs) -> object:
        """
        Parse NMEA byte stream to NMEAMessage object.

        :param bytes message: bytes message to parse
        :param int validate (kwarg): bitfield validation flags - VALCKSUM (default), VALMSGID (can be OR'd)
        :param int msgmode (kwarg): 0 = GET (default), 1 = SET, 2 = POLL
        :return: NMEAMessage object (or None if unknown message and VALMSGID is not set)
        :rtype: NMEAMessage
        :raises: NMEAParseError (if data stream contains invalid data or unknown message type)

        """

        validate = kwargs.get("validate", VALCKSUM)
        msgmode = kwargs.get("msgmode", 0)
        if msgmode not in (0, 1, 2):
            raise nme.NMEAParseError(
                f"Invalid parse mode {msgmode} - must be 0, 1 or 2."
            )

        try:
            talker, msgid, payload, checksum = get_parts(message)
            if validate & VALCKSUM:
                if not isvalid_cksum(message):
                    raise nme.NMEAParseError(
                        f"Message {talker}{msgid} invalid checksum {checksum}"
                        f" - should be {calc_checksum(message)}."
                    )
            return NMEAMessage(
                talker, msgid, msgmode, payload=payload, checksum=checksum
            )

        except nme.NMEAMessageError as err:
            if not validate & VALMSGID:
                return None
            raise nme.NMEAParseError(err)
