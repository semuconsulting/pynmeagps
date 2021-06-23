"""
This example illustrates a simple HTTP wrapper around pynmneagps.

It displays selected GPS data on a dynamically updated web page 
using the native Python 3 http.server library and a RESTful API
implemented by the pynmeagps streaming and parsing service.

Created on 17 May 2021

:author: semuadmin
:license: (c) SEMU Consulting 2021 - BSD 3-Clause License
"""

from io import BufferedReader
from threading import Thread
from time import sleep
import json
from gpshttpserver import GPSHTTPServer, GPSHTTPHandler, ADDRESS, TCPPORT
from serial import Serial, SerialException, SerialTimeoutException
from pynmeagps import NMEAReader, GET
import pynmeagps.exceptions as nme


class NMEAStreamer:
    """
    NMEAStreamer class.
    """

    def __init__(self, port, baudrate, timeout=0.1, nmea_only=0, validate=1):
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
        self.gpsdata = {
            "date": "1900-01-01",
            "time": "11.11.11",
            "latitude": 0.0,
            "longitude": 0.0,
            "elevation": 0.0,
            "speed": 0.0,
            "track": 0.0,
            "siv": 0,
            "pdop": 99,
            "hdop": 99,
            "vdop": 99,
            "fix": 0,
        }

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
            print(f"Connecting to serial port {self._port} at {self._baudrate} baud...")
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
            print("Disconnecting from serial port...")
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
            print("\nStarting reader thread...")
            self._reading = True
            self._serial_thread = Thread(target=self._read_thread, daemon=True)
            self._serial_thread.start()

    def stop_read_thread(self):
        """
        Stop the serial reader thread.
        """

        if self._serial_thread is not None:
            print("\nStopping web server thread...")
            self._reading = False

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
                        self.set_data(parsed_data)
                except (
                    nme.NMEAStreamError,
                    nme.NMEAMessageError,
                    nme.NMEATypeError,
                    nme.NMEAParseError,
                ) as err:
                    print(f"Something went wrong {err}")
                    continue

    def set_data(self, parsed_data):
        """
        Set GPS data dictionary.
        """

        print(parsed_data)
        if parsed_data.msgID == "RMC":
            self.gpsdata["date"] = str(parsed_data.date)
            self.gpsdata["time"] = str(parsed_data.time)
            self.gpsdata["latitude"] = parsed_data.lat
            self.gpsdata["longitude"] = parsed_data.lon
            self.gpsdata["speed"] = parsed_data.spd
            self.gpsdata["track"] = parsed_data.cog
        if parsed_data.msgID == "GGA":
            self.gpsdata["time"] = str(parsed_data.time)
            self.gpsdata["latitude"] = parsed_data.lat
            self.gpsdata["longitude"] = parsed_data.lon
            self.gpsdata["elevation"] = parsed_data.alt
            self.gpsdata["siv"] = parsed_data.numSV
            self.gpsdata["hdop"] = parsed_data.HDOP
        if parsed_data.msgID == "GSA":
            self.gpsdata["fix"] = parsed_data.navMode
            self.gpsdata["pdop"] = parsed_data.PDOP
            self.gpsdata["hdop"] = parsed_data.HDOP
            self.gpsdata["vdop"] = parsed_data.VDOP

    def get_data(self):
        """
        Return GPS data in JSON format.

        This is used by the RESTful API implemented in the
        GPSHTTPServer class.
        """

        return json.dumps(self.gpsdata)


if __name__ == "__main__":

    # Edit these for your GPS device
    SERIALPORT = "/dev/tty.usbmodem142101"
    BAUD = 38400

    nms = NMEAStreamer(SERIALPORT, BAUD)
    httpd = GPSHTTPServer((ADDRESS, TCPPORT), GPSHTTPHandler, nms)

    if nms.connect():
        nms.start_read_thread()
        httpd_thread = Thread(target=httpd.serve_forever, daemon=True)
        httpd_thread.start()

        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("\n\nInterrupted by user\n\n")

        httpd.shutdown()
        nms.stop_read_thread()
        sleep(2)  # wait for shutdown
        nms.disconnect()
        print("\nTest Complete")
