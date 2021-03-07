"""
Simple command line utility to stream the parsed NMEA output of an NMEA GNSS device.

Usage (all args are optional):
nmeadump.py port="COM6" baud=9600 timeout=5 nmea_only=0 raw=0

If nmea_only=True (1), streaming will terminate on any non-NMEA data.
"""

import sys
from serial import Serial
from pynmeagps.nmeareader import NMEAReader

PORT = "COM6"
BAUD = 9600
TIMEOUT = 5


def stream_ubx(**kwargs):
    """
    Stream output
    """

    try:
        port = kwargs.get("port", PORT).strip('"')
        baud = int(kwargs.get("baud", BAUD))
        timeout = int(kwargs.get("timeout", TIMEOUT))
        nmea_only = int(kwargs.get("nmea_only", 0))
        rawformat = int(kwargs.get("raw", 0))
        print(
            f"\nStreaming from {port} at {baud} baud in",
            f"{'raw' if rawformat else 'parsed'} format...\n",
        )
        stream = Serial(port, baud, timeout=timeout)
        nmr = NMEAReader(stream, nmea_only)
        for (raw, parsed) in nmr:
            if rawformat:
                print(raw)
            else:
                print(parsed)
    except KeyboardInterrupt:
        print("\nStreaming terminated by user\n")


if __name__ == "__main__":

    if len(sys.argv) > 1:
        if sys.argv[1] in {"-h", "--h", "help", "-help", "--help", "-H"}:
            print(
                " nmeadump.py is a simple command line utility to stream",
                "the parsed NMEA output of an NMEA GNSS device.\n\n",
                "Usage (all args are optional): nmeadump.py",
                'port="COM6" baud=9600 timeout=5',
                "nmea_only=0 raw=0\n\n Type Ctrl-C to terminate.",
            )
            sys.exit()

    stream_ubx(**dict(arg.split("=") for arg in sys.argv[1:]))
