"""
Simple command line utility to stream the parsed NMEA output of an NMEA GNSS device.

Usage (all args are optional):
nmeadump port="/dev/ttyACM1" baud=9600 timeout=5 nmea_only=0 validate=1 raw=0

If nmea_only=True (1), streaming will terminate on any non-NMEA data.
If validate & 1, will check for valid checksum (otherwise will ignore during reading, 
but possibly fail later during parsing if message is corrupt).
If validate & 2, will check for valid msgId (otherwise will ignore).
"""

import sys
from serial import Serial
from pynmeagps import NMEAReader, GET, VALCKSUM

# Default port settings - amend as required
PORT = "/dev/ttyACM1"
BAUD = 9600
TIMEOUT = 5


def stream_nmea(**kwargs):
    """
    Stream output to terminal.

    :param int port (kwarg): baud rate (/dev/ttyACM1)
    :param int baud (kwarg): baud rate (9600)
    :param int timeout (kwarg): timeout in seconds (5)
    :param int nmea_only (kwarg): set to True to generate error on non-NMEA data (0)
    :param int validate (kwarg): validate checksum (1)
    :param int raw (kwarg): set to True to output raw binary data (0)
    :raises: NMEAStreamError (if nmeaonly flag is 1 and stream contains non-NMEA data)

    """

    try:
        port = kwargs.get("port", PORT).strip('"')
        baud = int(kwargs.get("baud", BAUD))
        timeout = int(kwargs.get("timeout", TIMEOUT))
        nmea_only = int(kwargs.get("nmea_only", 0))
        validate = int(kwargs.get("validate", VALCKSUM))
        rawformat = int(kwargs.get("raw", 0))
        print(
            f"\nStreaming from {port} at {baud} baud in",
            f"{'raw' if rawformat else 'parsed'} format...\n",
        )
        stream = Serial(port, baud, timeout=timeout)
        nmr = NMEAReader(stream, nmeaonly=nmea_only, validate=validate, msgmode=GET)
        for (raw, parsed) in nmr:
            if rawformat:
                print(raw)
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
                "Usage (all args are optional): nmeadump.py",
                f"port={PORT} baud={BAUD} timeout={TIMEOUT}",
                "nmea_only=0 validate=1 raw=0\n\n Type Ctrl-C to terminate.",
            )
            sys.exit()

    stream_nmea(**dict(arg.split("=") for arg in sys.argv[1:]))


if __name__ == "__main__":

    main()
