"""
Example implementation of a NMEAMessage file reader
using the NMEAReader iterator functions

Created on 7 Mar 2021

@author: semuadmin
"""

from pynmeagps import NMEAReader, VALCKSUM, GET
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
        self._ubxreader = None
        self._connected = False
        self._reading = False

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

    def reader(self, nmea_only=False, validate=VALCKSUM, msgmode=GET):
        """
        Reads and parses NMEA message data from stream
        using NMEAReader iterator method
        """

        i = 0
        self._ubxreader = NMEAReader(
            self._stream, nmeaonly=nmea_only, validate=validate, msgmode=msgmode
        )

        for msg in self._ubxreader:  # invokes iterator method
            try:
                (raw_data, parsed_data) = msg
                #                 if raw_data:
                #                     print(raw_data)
                if parsed_data:
                    print(parsed_data)
                    i += 1
            except (ube.NMEAMessageError, ube.NMEATypeError, ube.NMEAParseError) as err:
                print(f"Something went wrong {err}")
                continue

        print(f"\n\n{i} message{'' if i == 1 else 's'} read from {self._filename}.")


if __name__ == "__main__":

    YES = ("Y", "y", "YES,", "yes", "True")
    NO = ("N", "n", "NO,", "no", "False")

    print("Enter fully qualified name of file containing binary NMEA data: ", end="")
    filefqn = input().strip('"')
    print("Do you want to ignore any non-NMEA data (y/n)? (y) ", end="")
    val = input() or "y"
    nmeaonly = val in NO
    print("Do you want to validate the message checksums ((y/n)? (y) ", end="")
    val = input() or "y"
    val1 = val in YES
    print(
        "Do you want to validate message IDs (i.e. raise an error if message ID is unknown) (y/n)? (n) ",
        end="",
    )
    val = input() or "n"
    val1 = 2 * val in YES
    vald = val1 + val1
    print("Message mode (0=GET (output), 1=SET (input), 2=POLL (poll)? (0) ", end="")
    mode = input() or "0"
    moded = int(mode)

    print("Instantiating NMEAStreamer class...")
    ubf = NMEAStreamer(filefqn)
    print(f"Opening file {filefqn}...")
    if ubf.open():
        print("Starting file reader")
        ubf.reader(nmeaonly, vald, moded)
        print("\n\nClosing file...")
        ubf.close()
        print("Test Complete")
