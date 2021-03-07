"""
Example implementation of a threaded NMEAMessage streamer.

Connects to the receiver's serial port and sets up a
daemon NMEAReader thread. While the thread is running in the
background, it sends a series of NMEA RMC POLL requests
corresponding to different GNSS constellations ('GPQ' = GPS, 
'GLQ' = GLONASS, etc.).

If the POLL is accepted, you'll see an RMC message in response (mixed
in with whatever other messages the receiver is sending periodically).

If the POLL is rejected, you'll typically get a TXT response:
"<NMEA(GNTXT, numMsg=1, msgNum=1, msgType=1, text=NMEA unknown msg)>"

The example is purely illustrative and the responses will depend
on your receiver's specific configuration and capabilities. A standard
domestic GPS receiver may typically only respond to the generic 'GNQ'
(any GNSS) POLL.

Created on 7 Mar 2021

@author: semuadmin
"""

from sys import platform
from io import BufferedReader
from threading import Thread
from time import sleep

from pynmeagps import NMEAReader, NMEAMessage, POLL
from serial import Serial, SerialException, SerialTimeoutException

import pynmeagps.exceptions as nme


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
        self._nmeareader = None
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
            self._nmeareader = NMEAReader(BufferedReader(self._serial_object), False)
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

    # set PORT, BAUDRATE and TIMEOUT as appropriate
    if platform == "win32":
        PORT = "COM6"
    else:
        PORT = "/dev/tty.usbmodem14101"
    BAUDRATE = 38400
    TIMEOUT = 1

    print("Instantiating NMEAStreamer class...")
    nms = NMEAStreamer(PORT, BAUDRATE, TIMEOUT)
    print(f"Connecting to serial port {PORT} at {BAUDRATE} baud...")
    nms.connect()
    print("Starting reader thread...")
    nms.start_read_thread()

    # DO OTHER STUFF HERE WHILE THREAD RUNS IN BACKGROUND...
    for mid in ('GAQ', 'GBQ', 'GLQ', 'GNQ', 'GPQ', 'GQQ'):
        print(f"\nSending a {mid} message to poll for an RMC response.")
        print("Look out for an RMC (known) or TXT (unknown) message in the input stream...\n")
        msg = NMEAMessage('EI', mid, POLL, msgId='RMC')
        nms.send(msg.serialize())
        sleep(3)

    print("\n\nStopping reader thread...")
    nms.stop_read_thread()
    print("Disconnecting from serial port...")
    nms.disconnect()
    print("Test Complete")
