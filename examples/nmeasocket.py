"""
nmeasocket.py

A simple example implementation of a GNSS socket reader
using the pynmeagps.NMEAReader iterator functions.

Usage:

python3 nmeasocket.py ipaddress=127.0.0.1 ipport=50012

Created on 05 May 2022
@author: semuadmin
"""

import socket
from sys import argv
from datetime import datetime

from pynmeagps.nmeareader import NMEAReader


def main(**kwargs):
    """
    Reads and parses NMEA message from socket stream.
    """

    count = 0
    start = datetime.now()

    ipaddress = kwargs.get("ipaddress", "localhost")
    ipport = int(kwargs.get("ipport", 50012))

    try:
        print(f"Opening socket {ipaddress}:{ipport}...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as stream:
            stream.connect((ipaddress, ipport))
            print("Starting NMEA reader...")
            nmr = NMEAReader(stream)
            for _, parsed_data in nmr:
                print(parsed_data)
                count += 1
    except KeyboardInterrupt:
        dur = datetime.now() - start
        secs = dur.seconds + dur.microseconds / 1e6
        print("Session terminated by user")
        print(
            f"{count:,d} messages read in {secs:.2f} seconds:",
            f"{count/secs:.2f} msgs per second",
        )


if __name__ == "__main__":

    main(**dict(arg.split("=") for arg in argv[1:]))
