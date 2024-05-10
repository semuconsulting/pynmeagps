"""
nmeafile.py

This example illustrates a simple implementation of a
NMEAMessage logfile reader using the
NMEAReader iterator functions and an external error handler.

Usage:

python3 nmeafile.py filename="nmeadata.log"

Created on 7 Mar 2021
@author: semuadmin
"""

from sys import argv

from pynmeagps.nmeareader import NMEAReader


def errhandler(err):
    """
    Handles errors output by iterator.
    """

    print(f"\nERROR: {err}\n")


def main(**kwargs):
    """
    Main routine.
    """

    filename = kwargs.get("filename", "nmeadata.log")

    count = 0
    print(f"\nOpening file {filename}...\n")
    with open(filename, "rb") as stream:
        nmr = NMEAReader(
            stream, nmeaonly=False, quitonerror=False, errorhandler=errhandler
        )
        for raw, parsed_data in nmr:
            print(parsed_data)
            count += 1

    print(f"\n{count} messages read.\n")
    print("\nProcessing Complete")


if __name__ == "__main__":

    main(**dict(arg.split("=") for arg in argv[1:]))
