"""
Example implementation of a threaded NMEAMessage streamer

Connects to the receiver's serial port and sets up a
threaded NMEAReader process. It waits for 10 seconds,
then terminates the thread.

Created on 2 Oct 2020

@author: semuadmin
"""

from sys import platform
from io import BufferedReader
from threading import Thread
from time import sleep

from pynmeagps.nmeareader import NMEAReader
from serial import Serial, SerialException, SerialTimeoutException

import pynmeagps.exceptions as ube


class NMEAStreamer:
    """
    NMEAStreamer class.
    """

    def __init__(self, port, baudrate, timeout=5):
        """
        Constructor.
        """

        self._serial_object = None
        self._serial_thread = None
        self._ubxreader = None
        self._connected = False
        self._reading = False
        self._port = port
        self._baudrate = baudrate
        self._timeout = timeout

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

        try:
            self._serial_object = Serial(
                self._port, self._baudrate, timeout=self._timeout
            )
            self._ubxreader = NMEAReader(BufferedReader(self._serial_object), False)
            self._connected = True
        except (SerialException, SerialTimeoutException) as err:
            print(f"Error connecting to serial port {err}")

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
                    (raw_data, parsed_data) = self._ubxreader.read()
                    if parsed_data:
                        print(parsed_data)
                except (
                    ube.NMEAStreamError,
                    ube.NMEAMessageError,
                    ube.NMEATypeError,
                    ube.NMEAParseError,
                ) as err:
                    print(f"Something went wrong {err}")
                    continue


if __name__ == "__main__":

    # set PORT, BAUDRATE and TIMEOUT as appropriate
    if platform == "win32":
        PORT = "COM6"
    else:
        PORT = "/dev/tty.usbmodem14101"
    BAUDRATE = 38400
    TIMEOUT = 1

    print("Instantiating NMEAStreamer class...")
    ubp = NMEAStreamer(PORT, BAUDRATE, TIMEOUT)
    print(f"Connecting to serial port {PORT} at {BAUDRATE} baud...")
    ubp.connect()
    print("Starting reader thread...")
    ubp.start_read_thread()

    # DO OTHER STUFF HERE WHILE THREAD RUNS IN BACKGROUND...
    sleep(10)

    print("\n\nStopping reader thread...")
    ubp.stop_read_thread()
    print("Disconnecting from serial port...")
    ubp.disconnect()
    print("Test Complete")
