"""
Simple command line utility to stream the parsed NMEA output of an NMEA GNSS device
to the terminal.

Usage (all args are optional):
nmeadump port="/dev/ttyACM1" baud=9600 timeout=5 nmea_only=0 validate=1 output=0 filter=*

output: 0 = parsed format, 1 = binary format, 2 = hexadecimal format

If nmea_only=True (1), streaming will terminate on any non-NMEA data.
If validate & 1, will check for valid checksum (otherwise will ignore during reading, 
but possibly fail later during parsing if message is corrupt).
If validate & 2, will check for known valid msgId (otherwise will ignore).

Created on 22 Aug 2021

:author: semuadmin
:copyright: SEMU Consulting © 2021
:license: BSD 3-Clause
"""

import sys
from serial import Serial
from pynmeagps import NMEAReader, GET, VALCKSUM

# Output formats
PARSED = 0
BIN = 1
HEX = 2

# Default port settings - amend as required
PORT = "/dev/ttyACM1"
BAUD = 9600
TIMEOUT = 5


def stream_nmea(**kwargs):
    """
    Stream output to terminal.

    :param str port (kwarg): baud rate (/dev/ttyACM1)
    :param int baud (kwarg): baud rate (9600)
    :param int timeout (kwarg): timeout in seconds (5)
    :param int nmea_only (kwarg): set to True to generate error on non-NMEA data (0)
    :param int validate (kwarg): validate checksum (1)
    :param int output (kwarg): 0=Parsed, 1=Binary, 2=Hexadecimal (0)
    :param str filter (kwarg): comma-separated list of specific NMEA msgIDs to display (*)
    :raises: NMEAStreamError (if nmeaonly flag is 1 and stream contains non-NMEA data)

    """

    try:
        port = kwargs.get("port", PORT).strip('"')
        baud = int(kwargs.get("baud", BAUD))
        timeout = int(kwargs.get("timeout", TIMEOUT))
        nmea_only = int(kwargs.get("nmea_only", 0))
        validate = int(kwargs.get("validate", VALCKSUM))
        output = int(kwargs.get("output", PARSED))
        filter = kwargs.get("filter", "*")
        filtertxt = "" if filter == "*" else f", filtered by {filter}"
        print(
            f"\nStreaming from {port} at {baud} baud in",
            f"{['parsed','binary','xexadecimal'][output]} format{filtertxt}...\n",
        )
        stream = Serial(port, baud, timeout=timeout)
        nmr = NMEAReader(stream, nmeaonly=nmea_only, validate=validate, msgmode=GET)
        for (raw, parsed) in nmr:
            if filter == "*" or parsed.msgID in filter:
                if output == BIN:
                    print(raw)
                elif output == HEX:
                    print(raw.hex())
                else:
                    print(parsed)
    except KeyboardInterrupt:
        print("\nStreaming terminated by user\n")


def main():
    """
    CLI Entry point

    args as stream_nmea() method
    """

    if len(sys.argv) > 1:
        if sys.argv[1] in {"-h", "--h", "help", "-help", "--help", "-H"}:
            print(
                " nmeadump is a simple command line utility to stream",
                "the parsed NMEA output of an NMEA GNSS device.\n\n",
                "Usage (all args are optional): nmeadump",
                f"port={PORT} baud={BAUD} timeout={TIMEOUT}",
                "nmea_only=0 validate=1 output=0 filter=*\n\n Type Ctrl-C to terminate.",
            )
            sys.exit()

    stream_nmea(**dict(arg.split("=") for arg in sys.argv[1:]))


if __name__ == "__main__":

    main()
