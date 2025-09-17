"""
Socket reader tests for pynmeagps - uses dummy socket class
to achieve 99% test coverage of SocketStream.

Created on 11 May 2022

*** NB: must be saved in UTF-8 format ***

:author: semuadmin (Steve Smith)
"""

import unittest
from socket import socket
from pynmeagps import NMEAReader, NMEAMessage, POLL


class DummySocket(socket):
    """
    Dummy socket class which simulates recv() method
    and TimeoutError.
    """

    def __init__(self, *args, **kwargs):
        self._timeout = False
        if "timeout" in kwargs:
            self._timeout = kwargs["timeout"]
            kwargs.pop("timeout")

        super().__init__(*args, **kwargs)

        pool = (
            b"\xb5b\x06\x8b\x0c\x00\x00\x00\x00\x00\x68\x00\x11\x40\xb6\xf3\x9d\x3f\xdb\x3d"
            + b"\xb5b\x10\x02\x1c\x00\x6d\xd8\x07\x00\x18\x20\x00\x00\xcd\x06\x00\x0e\xe4\xfe\xff\x0d\x03\xfa\xff\x05\x09\x0b\x00\x0c\x6d\xd8\x07\x00\xee\x51"
            + b"\xb5b\x10\x02\x18\x00\x72\xd8\x07\x00\x18\x18\x00\x00\x4b\xfd\xff\x10\x40\x02\x00\x11\x23\x28\x00\x12\x72\xd8\x07\x00\x03\x9c"
            + b"$GNDTM,W84,,0.0,N,0.0,E,0.0,W84*71\r\n"
            + b"$GNRMC,103607.00,A,5327.03942,N,10214.42462,W,0.046,,060321,,,A,V*0E\r\n"
            + b"$GPRTE,2,1,c,0,PBRCPK,PBRTO,PTELGR,PPLAND,PYAMBU,PPFAIR,PWARRN,PMORTL,PLISMR*73\r\n"
            + b"\xd3\x00\x13\x3e\xd7\xd3\x02\x02\x98\x0e\xde\xef\x34\xb4\xbd\x62\xac\x09\x41\x98\x6f\x33\x36\x0b\x98"
            + b"\xd3\x00\x13>\xd0\x00\x03\x8aX\xd9I<\x87/4\x10\x9d\x07\xd6\xafH Z\xd7\xf7"
            + b"\xd3\x00\x12B\x91\x81\xc9\x84\x00\x04B\xb8\x88\x008\x80\t\xd0F\x00(\xf0kf"
        )
        self._stream = pool * round(4096 / len(pool))
        self._buffer = self._stream

    def recv(self, num: int) -> bytes:
        if self._timeout:
            raise TimeoutError
        if len(self._buffer) < num:
            self._buffer = self._buffer + self._stream
        buff = self._buffer[:num]
        self._buffer = self._buffer[num:]
        return buff

    def send(self, data: bytes):
        if self._timeout:
            raise TimeoutError
        return None


class SocketTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    # *******************************************
    # Helper methods
    # *******************************************

    def testSocketStub(self):
        EXPECTED_RESULTS = (
            "<NMEA(GNDTM, datum=W84, subDatum=, latOfset=0.0, NS=N, lonOfset=0.0, EW=E, alt=0.0, refDatum=W84)>",
            "<NMEA(GNRMC, time=10:36:07, status=A, lat=53.450657, NS=N, lon=-102.2404103333, EW=W, spd=0.046, cog=, date=2021-03-06, mv=, mvEW=, posMode=A, navStatus=V)>",
            "<NMEA(GPRTE, numMsg=2, msgNum=1, status=c, routeid=0, wpt_01=PBRCPK, wpt_02=PBRTO, wpt_03=PTELGR, wpt_04=PPLAND, wpt_05=PYAMBU, wpt_06=PPFAIR, wpt_07=PWARRN, wpt_08=PMORTL, wpt_09=PLISMR)>",
            "<NMEA(GNDTM, datum=W84, subDatum=, latOfset=0.0, NS=N, lonOfset=0.0, EW=E, alt=0.0, refDatum=W84)>",
            "<NMEA(GNRMC, time=10:36:07, status=A, lat=53.450657, NS=N, lon=-102.2404103333, EW=W, spd=0.046, cog=, date=2021-03-06, mv=, mvEW=, posMode=A, navStatus=V)>",
            "<NMEA(GPRTE, numMsg=2, msgNum=1, status=c, routeid=0, wpt_01=PBRCPK, wpt_02=PBRTO, wpt_03=PTELGR, wpt_04=PPLAND, wpt_05=PYAMBU, wpt_06=PPFAIR, wpt_07=PWARRN, wpt_08=PMORTL, wpt_09=PLISMR)>",
            "<NMEA(GNDTM, datum=W84, subDatum=, latOfset=0.0, NS=N, lonOfset=0.0, EW=E, alt=0.0, refDatum=W84)>",
            "<NMEA(GNRMC, time=10:36:07, status=A, lat=53.450657, NS=N, lon=-102.2404103333, EW=W, spd=0.046, cog=, date=2021-03-06, mv=, mvEW=, posMode=A, navStatus=V)>",
            "<NMEA(GPRTE, numMsg=2, msgNum=1, status=c, routeid=0, wpt_01=PBRCPK, wpt_02=PBRTO, wpt_03=PTELGR, wpt_04=PPLAND, wpt_05=PYAMBU, wpt_06=PPFAIR, wpt_07=PWARRN, wpt_08=PMORTL, wpt_09=PLISMR)>",
            "<NMEA(GNDTM, datum=W84, subDatum=, latOfset=0.0, NS=N, lonOfset=0.0, EW=E, alt=0.0, refDatum=W84)>",
            "<NMEA(GNRMC, time=10:36:07, status=A, lat=53.450657, NS=N, lon=-102.2404103333, EW=W, spd=0.046, cog=, date=2021-03-06, mv=, mvEW=, posMode=A, navStatus=V)>",
            "<NMEA(GPRTE, numMsg=2, msgNum=1, status=c, routeid=0, wpt_01=PBRCPK, wpt_02=PBRTO, wpt_03=PTELGR, wpt_04=PPLAND, wpt_05=PYAMBU, wpt_06=PPFAIR, wpt_07=PWARRN, wpt_08=PMORTL, wpt_09=PLISMR)>",
        )
        raw = None
        stream = DummySocket()
        nmr = NMEAReader(stream, bufsize=1024)
        buff = nmr._stream.buffer  # test buffer getter method
        i = 0
        for raw, parsed in nmr:
            if raw is not None:
                # print(parsed)
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1
                if i >= 12:
                    break
        self.assertEqual(i, 12)

    def testSocketSend(self):
        stream = DummySocket()
        nmr = NMEAReader(stream, bufsize=1024)
        msg = NMEAMessage("EI", "GNQ", POLL, msgId="RMC")
        res = nmr.datastream.write(msg.serialize())
        self.assertEqual(res, None)

    def testSocketIter(self):  # test for extended stream
        raw = None
        stream = DummySocket()
        nmr = NMEAReader(stream)
        i = 0
        for raw, parsed in nmr:
            if raw is None:
                raise EOFError
            i += 1
            if i >= 123:
                break
        self.assertEqual(i, 123)

    def testSocketError(self):  # test for simulated socket timeout
        raw = None
        stream = DummySocket(timeout=True)
        nmr = NMEAReader(stream)
        i = 0
        for raw, parsed in nmr:
            i += 1
            if i >= 12:
                break
        self.assertEqual(i, 0)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
