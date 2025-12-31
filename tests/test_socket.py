"""
Socket reader tests for pynmeagps - uses dummy socket class
to achieve 99% test coverage of SocketStream.

Created on 11 May 2022

*** NB: must be saved in UTF-8 format ***

:author: semuadmin (Steve Smith)
"""

import unittest
from socket import socket
from pynmeagps import (
    NMEAReader,
    NMEAMessage,
    POLL,
    ENCODE_CHUNKED,
    ENCODE_NONE,
    DEFAULT_BUFSIZE,
    SocketWrapper,
)


def chunk(data: bytes, chunksize: int = 10) -> bytes:
    """
    Test method to chunk encode a byte stream
    """

    ckb = f"{chunksize:x}\r\n".encode("ascii")
    output = b""
    eod = False
    pos = 0
    while not eod:
        if len(data[pos : pos + chunksize]) < chunksize:
            eod = True
        output += ckb + data[pos : pos + chunksize] + b"\r\n"
        pos += chunksize
    output += b"0\r\n\r\n"
    return output


SOCKETPOOL = (
    b"$GNDTM,W84,,0.0,N,0.0,E,0.0,W84*71\r\n"
    b"$GNRMC,103607.00,A,5327.03942,N,10214.42462,W,0.046,,060321,,,A,V*0E\r\n"
    b"$GPRTE,2,1,c,0,PBRCPK,PBRTO,PTELGR,PPLAND,PYAMBU,PPFAIR,PWARRN,PMORTL,PLISMR*73\r\n"
) * 10

SOCKETPOOL_CHUNKED = chunk(SOCKETPOOL)


class DummySocket(socket):
    """
    Dummy socket class which simulates recv() method
    and TimeoutError.
    """

    def __init__(self, pool: bytes, *args, **kwargs):

        self._timeout = kwargs.pop("timeout", False)

        super().__init__(*args, **kwargs)

        self._stream = pool * round(DEFAULT_BUFSIZE / len(pool))
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

    def testSocketWrapper(self):  # test SocketWrapper getters

        stream = DummySocket(SOCKETPOOL)
        sw = SocketWrapper(stream)
        self.assertIsInstance(sw.buffer, bytearray)
        self.assertEqual(sw.in_waiting(), 4096)

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
        stream = DummySocket(SOCKETPOOL)
        nmr = NMEAReader(stream, encoding=ENCODE_NONE, bufsize=1024)
        buff = nmr._stream.buffer  # test buffer getter method
        i = 0
        for raw, parsed in nmr:
            if raw is not None:
                # print(f'"{parsed}",')
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1
                if i >= 12:
                    break
        self.assertEqual(i, 12)

    def testSocketChunked(self):
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
        stream = DummySocket(SOCKETPOOL_CHUNKED)
        nmr = NMEAReader(stream, encoding=ENCODE_CHUNKED, bufsize=1024)
        buff = nmr._stream.buffer  # test buffer getter method
        i = 0
        for raw, parsed in nmr:
            if raw is not None:
                # print(f'"{parsed}",')
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1
                if i >= 12:
                    break
        self.assertEqual(i, 12)

    def testSocketSend(self):
        stream = DummySocket(SOCKETPOOL)
        nmr = NMEAReader(stream, bufsize=1024)
        msg = NMEAMessage("EI", "GNQ", POLL, msgId="RMC")
        res = nmr.datastream.write(msg.serialize())
        self.assertEqual(res, None)

    def testSocketIter(self):  # test for extended stream
        raw = None
        stream = DummySocket(SOCKETPOOL)
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
        stream = DummySocket(SOCKETPOOL, timeout=True)
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
