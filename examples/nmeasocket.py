"""
nmeasocket.py

A simple example implementation of a GNSS socket reader
using the pynmeagps.UBXReader iterator functions.

Created on 05 May 2022
@author: semuadmin
"""

import socket
from datetime import datetime
from pynmeagps.nmeareader import NMEAReader


def read(stream: socket.socket):
    """
    Reads and parses NMEA message from socket stream.
    """

    msgcount = 0
    start = datetime.now()

    nmr = NMEAReader(
        stream,
    )
    try:
        for (_, parsed_data) in nmr.iterate():
            print(parsed_data)
            msgcount += 1
    except KeyboardInterrupt:
        dur = datetime.now() - start
        secs = dur.seconds + dur.microseconds / 1e6
        print("Session terminated by user")
        print(
            f"{msgcount:,d} messages read in {secs:.2f} seconds:",
            f"{msgcount/secs:.2f} msgs per second",
        )


if __name__ == "__main__":

    SERVER = "localhost"
    PORT = 50007

    print(f"Opening socket {SERVER}:{PORT}...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((SERVER, PORT))
        read(sock)
