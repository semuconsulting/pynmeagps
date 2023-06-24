"""
nmeafile.py

This example illustrates a simple implementation of a
NMEAMessage logfile reader using the
NMEAReader iterator functions and an external error handler.

Created on 7 Mar 2021
@author: semuadmin
"""

from pynmeagps.nmeareader import NMEAReader


def errhandler(err):
    """
    Handles errors output by iterator.
    """

    print(f"\nERROR: {err}\n")


def read(stream, errorhandler):
    """
    Reads and parses UBX message data from stream.
    """
    # pylint: disable=unused-variable

    msgcount = 0

    nmr = NMEAReader(
        stream, nmeaonly=False, quitonerror=False, errorhandler=errorhandler
    )
    for raw, parsed_data in nmr:
        print(parsed_data)
        msgcount += 1

    print(f"\n{msgcount} messages read.\n")


if __name__ == "__main__":
    print("\nEnter fully qualified name of file containing raw NMEA data: ", end="")
    filename = input().strip('"')

    print(f"\nOpening file {filename}...\n")
    with open(filename, "rb") as fstream:
        read(fstream, errhandler)
    print("\nProcessing Complete")
