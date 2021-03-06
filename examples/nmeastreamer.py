"""
Threaded NMEAMessage streamer which polls for every currently
recognised standard NMEA message type.

Connects to the receiver's serial port and sets up a
daemon NMEAReader thread. While the thread is running in the
background, it sends a GNQ poll request for every currently
documented standard NMEA message type.

If the POLL is accepted, you'll see the requested message type in
response (mixed in with whatever other messages the receiver is
sending periodically - you might want to turn off periodic messaging
for the duration of this demo via your paticular receiver's
configuration facilities).

If the POLL is rejected, you'll typically get a TXT response:
"<NMEA(GNTXT, numMsg=1, msgNum=1, msgType=1, text=NMEA unknown msg)>"

The example is purely illustrative and the responses will depend
on your receiver's specific configuration and capabilities.

Created on 7 Mar 2021

@author: semuadmin
"""

from io import BufferedReader
from threading import Thread
from time import sleep

from pynmeagps import NMEAReader, NMEAMessage, POLL, GET, NMEA_MSGIDS
from serial import Serial, SerialException, SerialTimeoutException

import pynmeagps.exceptions as nme


class NMEAStreamer:
    """
    NMEAStreamer class.
    """

    def __init__(self, port, baudrate, timeout=5, nmea_only=0, validate=1):
        """
        Constructor.
        """

        self._serial_object = None
        self._serial_thread = None
        self._nmeareader = None
        self._connected = False
        self._reading = False
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout
        self._nmea_only = nmea_only
        self._validate = validate

    def __del__(self):
        """
        Destructor.
        """

        self.stop_read_thread()
        self.disconnect()

    def connect(self):
        """
        Open serial connection.
        """

        self._connected = False
        try:
            self._serial_object = Serial(
                self._port, self._baudrate, timeout=self._timeout
            )
            self._nmeareader = NMEAReader(
                BufferedReader(self._serial_object),
                nmeaonly=self._nmea_only,
                validate=self._validate,
                msgmode=GET,
            )
            self._connected = True
        except (SerialException, SerialTimeoutException) as err:
            print(f"Error connecting to serial port {err}")

        return self._connected

    def disconnect(self):
        """
        Close serial connection.
        """

        if self._connected and self._serial_object:
            try:
                self._serial_object.close()
            except (SerialException, SerialTimeoutException) as err:
                print(f"Error disconnecting from serial port {err}")
        self._connected = False

        return self._connected

    def start_read_thread(self):
        """
        Start the serial reader thread.
        """

        if self._connected:
            self._reading = True
            self._serial_thread = Thread(target=self._read_thread, daemon=True)
            self._serial_thread.start()

    def stop_read_thread(self):
        """
        Stop the serial reader thread.
        """

        if self._serial_thread is not None:
            self._reading = False

    def send(self, data):
        """
        Send data to serial connection.
        """

        self._serial_object.write(data)

    def flush(self):
        """
        Flush input buffer
        """

        self._serial_object.reset_input_buffer()

    def waiting(self):
        """
        Check if any messages remaining in the input buffer
        """

        return self._serial_object.in_waiting

    def _read_thread(self):
        """
        THREADED PROCESS
        Reads and parses NMEA message data from stream
        """

        while self._reading and self._serial_object:
            if self._serial_object.in_waiting:
                try:
                    (raw_data, parsed_data) = self._nmeareader.read()
                    if parsed_data:
                        print(parsed_data)
                except (
                    nme.NMEAStreamError,
                    nme.NMEAMessageError,
                    nme.NMEATypeError,
                    nme.NMEAParseError,
                ) as err:
                    print(f"Something went wrong {err}")
                    continue


if __name__ == "__main__":

    YES = ("Y", "y", "YES,", "yes", "True")
    NO = ("N", "n", "NO,", "no", "False")
    PAUSE = 1

    print("Enter port: ", end="")
    val = input().strip('"')
    prt = val
    print("Enter baud rate (9600): ", end="")
    val = input().strip('"') or "9600"
    baud = int(val)
    print("Enter timeout (0.1): ", end="")
    val = input().strip('"') or "0.1"
    timout = float(val)
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
    val2 = 2 * val in YES
    vald = val1 + val2

    print(f"Connecting to serial port {prt} at {baud} baud...")
    nms = NMEAStreamer(prt, baud, timout, nmeaonly, vald)
    if nms.connect():
        print("Starting reader thread...")
        nms.start_read_thread()

        # DO OTHER STUFF HERE WHILE THREAD RUNS IN BACKGROUND...
        for mid in NMEA_MSGIDS:
            print(f"\n\nSending a GNQ message to poll for an {mid} response...\n\n")
            msg = NMEAMessage("EI", "GNQ", POLL, msgId=mid)
            nms.send(msg.serialize())
            sleep(PAUSE)

        print("\n\nStopping reader thread...")
        nms.stop_read_thread()
        sleep(2)
        print("Disconnecting from serial port...")
        nms.disconnect()
        print("Test Complete")
