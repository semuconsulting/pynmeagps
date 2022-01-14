"""
Example implementation of a NMEAMessage file reader
using the NMEAReader iterator functions

Created on 7 Mar 2021

@author: semuadmin
"""

from pynmeagps import NMEAReader, VALCKSUM, VALMSGID, GET
import pynmeagps.exceptions as ube


class NMEAStreamer:
    """
    NMEAStreamer class.
    """

    def __init__(self, filename):
        """
        Constructor.
        """

        self._filename = filename
        self._stream = None
        self._nmeareader = None
        self._connected = False
        self._reading = False
        self._count = 0
        self._errors = 0

    def __del__(self):
        """
        Destructor.
        """

        self.close()

    def open(self):
        """
        Open file.
        """

        self._connected = False
        try:
            self._stream = open(self._filename, "rb")
            self._connected = True
        except Exception as err:
            print(f"Error opening file {err}")

        return self._connected

    def close(self):
        """
        Close file.
        """

        if self._connected and self._stream:
            try:
                self._stream.close()
            except Exception as err:
                print(f"Error closing file {err}")
        self._connected = False

        return self._connected

    def iterate(self, nmr):
        """
        Invoke read iterator.
        """

        while True:
            try:
                yield next(nmr)
                self._count += 1
            except StopIteration:
                break
            except (
                ube.NMEAMessageError,
                ube.NMEATypeError,
                ube.NMEAParseError,
                ube.NMEAStreamError,
            ) as err:
                print(f"\n\nSomething went wrong {err}\n\n")
                self._errors += 1
                continue

    def reader(self, nmea_only=False, validate=VALCKSUM, msgmode=GET):
        """
        Reads and parses NMEA message data from stream.
        """

        for (raw_data, parsed_data) in self.iterate(
            NMEAReader(self._stream, nmeaonly=nmea_only, validate=vald, msgmode=msgmode)
        ):
            print(parsed_data)

        print(
            f"\n\n{self._count} message{'' if self._count == 1 else 's'} read from {self._filename} with {self._errors} errors."
        )


if __name__ == "__main__":

    YES = ("Y", "y", "YES,", "yes", "True")
    NO = ("N", "n", "NO,", "no", "False")
    vald = 0

    print("Enter fully qualified name of file containing binary NMEA data: ", end="")
    filefqn = input().strip('"')
    print("Do you want to ignore any non-NMEA data (y/n)? (y) ", end="")
    val = input() or "y"
    nmeaonly = val in NO
    print("Do you want to validate the message checksums ((y/n)? (y) ", end="")
    val = input() or "y"
    if val in YES:
        vald = VALCKSUM
    print(
        "Do you want to validate message IDs (i.e. raise an error if message ID is unknown) (y/n)? (n) ",
        end="",
    )
    val = input() or "n"
    if val in YES:
        vald += VALMSGID
    print("Message mode (0=GET (output), 1=SET (input), 2=POLL (poll)? (0) ", end="")
    mode = input() or "0"
    moded = int(mode)

    print("Instantiating NMEAStreamer class...")
    ubf = NMEAStreamer(filefqn)
    print(f"Opening file {filefqn}...")
    if ubf.open():
        print("Starting file reader...")
        ubf.reader(nmeaonly, vald, moded)
        print("\n\nClosing file...")
        ubf.close()
        print("Test Complete")
