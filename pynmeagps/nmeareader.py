"""
NMEAReader class.

Reads and parses individual NMEA GNSS/GPS messages from
any stream which supports a read(n) -> bytes method.

Can also read from socket via SocketStream wrapper.

Returns both the raw binary data (as bytes) and the parsed
data (as a NMEAMessage object).

If the 'nmeaonly' kwarg is set to 'True', the reader
will raise a NMEAStreamerError if it encounters any non-NMEA
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
from pynmeagps.nmeatypes_core import NMEA_HDR, VALCKSUM


class NMEAReader:
    """
    NMEAReader class.
    """

    def __init__(self, stream, **kwargs):
        """Constructor.

        :param stream stream: input data stream (e.g. Serial or binary File)
        :param bool nmeaonly (kwarg): True = error on non-NMEA data, False = ignore non-NMEA data
        :param int validate (kwarg): bitfield validation flags - VALCKSUM (default), VALMSGID
        :param int msgmode (kwarg): 0 = GET (default), 1 = SET, 2 = POLL
        :param int bufsize: (kwarg) socket recv buffer size (4096)
        :raises: NMEAStreamError (if mode is invalid)

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
            raise nme.NMEAStreamError(
                f"Invalid stream mode {msgmode} - must be 0, 1 or 2."
            )
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
        if raw_data is not None:
            return (raw_data, parsed_data)
        raise StopIteration

    def read(self) -> (bytes, NMEAMessage):
        """
        Read the binary data from the stream buffer.

        :return: tuple of (raw_data as bytes, parsed_data as NMEAMessage)
        :rtype: tuple
        :raises: NMEAStreamError (if nmeaonly=True and stream includes non-NMEA data)

        """

        reading = True
        raw_data = None
        parsed_data = None

        while reading:  # loop until end of valid NMEA message or EOF
            byte1 = self._stream.read(1)  # read 1st byte
            if len(byte1) < 1:  # EOF
                break
            if byte1 != b"\x24":  # not NMEA, discard and continue
                continue
            byte2 = self._stream.read(1)  # read 2nd byte to confirm protocol
            if len(byte2) < 1:  # EOF
                break
            bytehdr = byte1 + byte2
            if bytehdr in NMEA_HDR:  # it's a NMEA message
                byten = self._stream.readline()  # NMEA protocol is CRLF terminated
                if byten[-2:] != b"\x0d\x0a":  # EOF
                    break
                raw_data = bytehdr + byten
                parsed_data = self.parse(
                    raw_data, validate=self._validate, msgmode=self._mode
                )
                reading = False
            else:  # it's not a NMEA message (UBX or something else)
                if self._nmea_only:  # raise error and quit
                    raise nme.NMEAStreamError(f"Unknown data header {bytehdr}.")

        return (raw_data, parsed_data)

    def iterate(self, **kwargs) -> tuple:
        """
        Invoke the iterator within an exception handling framework.

        :param bool quitonerror: (kwarg) Quit on NMEA error True/False (True)
        :param object errorhandler: (kwarg) Optional error handler (None)
        :return: tuple of (raw_data as bytes, parsed_data as NMEAMessage)
        :rtype: tuple
        :raises: NMEA...Error (if quitonerror is True and stream is invalid)

        """

        quitonerror = kwargs.get("quitonerror", True)
        errorhandler = kwargs.get("errorhandler", None)

        while True:
            try:
                yield next(self)
            except StopIteration:
                break
            except (
                nme.NMEAMessageError,
                nme.NMEATypeError,
                nme.NMEAParseError,
                nme.NMEAStreamError,
            ) as err:
                if quitonerror:
                    raise err
                if errorhandler is None:
                    print(err)
                else:
                    errorhandler(err)
                continue

    @staticmethod
    def parse(message: bytes, **kwargs) -> object:
        """
        Parse NMEA byte stream to NMEAMessage object.

        :param bytes message: bytes message to parse
        :param int validate (kwarg): bitfield validation flags - VALCKSUM (default), VALMSGID
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
            raise nme.NMEAParseError(err)
