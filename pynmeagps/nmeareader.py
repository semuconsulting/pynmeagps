"""
NMEAReader class.

Reads and parses individual NMEA GNSS/GPS messages from
any stream which supports a read(n) -> bytes method.

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

from pynmeagps.nmeamessage import NMEAMessage
import pynmeagps.exceptions as nme
from pynmeagps.nmeahelpers import (
    get_parts,
    calc_checksum,
    isvalid_cksum,
)

# parser validation flag values
VALNONE = 0
VALCKSUM = 1
VALMSGID = 2


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
        :raises: NMEAStreamError (if mode is invalid)

        """

        nmeaonly = kwargs.get("nmeaonly", False)
        validate = kwargs.get("validate", VALCKSUM)
        msgmode = kwargs.get("msgmode", 0)
        if msgmode not in (0, 1, 2):
            raise nme.NMEAStreamError(
                f"Invalid stream mode {msgmode} - must be 0, 1 or 2."
            )

        self._stream = stream
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

        byte1 = self._stream.read(1)  # read the first byte

        while reading:
            is_nmeas = False
            is_nmeap = False
            if len(byte1) < 1:  # EOF
                break
            if byte1 == b"\x24":
                byte2 = self._stream.read(1)
                if len(byte2) < 1:  # EOF
                    break
                if byte2 == b"\x47":
                    is_nmeas = True
                if byte2 == b"\x50":
                    is_nmeap = True
            if is_nmeas or is_nmeap:  # it's a NMEA message
                byten = self._stream.readline()
                raw_data = byte1 + byte2 + byten
                parsed_data = self.parse(
                    raw_data, validate=self._validate, msgmode=self._mode
                )
                reading = False
            else:  # it's not a NMEA message (UBX or something else)
                prevbyte = byte1
                byte1 = self._stream.read(1)
                if self._nmea_only:  # raise error and quit
                    raise nme.NMEAStreamError(
                        f"Unknown data header {prevbyte + byte1}."
                    )

        return (raw_data, parsed_data)

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
            if validate & VALMSGID:
                modestr = ["GET", "SET", "POLL"][msgmode]
                raise nme.NMEAParseError(
                    (
                        "Unknown or invalid message definition "
                        f"msgID {msgid}, talker {talker}, mode {modestr}."
                    )
                ) from err
            return None
