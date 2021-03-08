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

        try:
            self._stream = open(self._filename, "rb")
            self._connected = True
        except Exception as err:
            print(f"Error opening file {err}")

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

    def reader(self, nmea_only=False, validate=VALCKSUM, mode=GET):
        """
        Reads and parses NMEA message data from stream
        using NMEAReader iterator method
        """

        i = 0
        self._ubxreader = NMEAReader(self._stream, nmea_only, validate, mode)

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

    print("Enter fully qualified name of file containing binary NMEA data: ", end="")
    filefqn = input().strip('"')
    print("Do you want to ignore non-NMEA data (y/n)? (y) ", end="")
    val = input() or "y"
    NMEA_ONLY = val in ("N", "n", "NO,", "no", "False")
    print("Do you want to validate the data stream (0/1/2/3)? (1) ", end="")
    val = input() or "1"
    VALD = int(val)
    print("Message mode (0=GET (output), 1=SET (input), 2=POLL (poll)? (0) ", end="")
    moded = input() or "0"
    MODED = int(moded)

    print("Instantiating NMEAStreamer class...")
    ubf = NMEAStreamer(filefqn)
    print(f"Opening file {filefqn}...")
    ubf.open()
    print("Starting file reader")
    ubf.reader(NMEA_ONLY, VALD, MODED)
    print("\n\nClosing file...")
    ubf.close()
    print("Test Complete")
