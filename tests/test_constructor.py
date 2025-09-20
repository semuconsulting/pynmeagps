"""
Constructor method tests for pynmeagps

Created on 4 Mar 2021

*** NB: must be saved in UTF-8 format ***

:author: semuadmin (Steve Smith)
"""

import unittest
from datetime import datetime
from pynmeagps import (
    NMEAMessage,
    NMEAReader,
    GET,
    SET,
    POLL,
    NMEAMessageError,
    VALCKSUM,
    VALMSGID,
)


class FillTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def testFill_GNGLL(self):  # test GET constructor with full payload keyword
        EXPECTED_RESULT = "<NMEA(GNGLL, lat=-53.4507198333, NS=S, lon=2.2402326667, EW=E, time=22:32:32, status=A, posMode=A)>"
        res = NMEAMessage(
            "GN",
            "GLL",
            GET,
            payload=["5327.04319", "S", "00214.41396", "E", "223232.00", "A", "A"],
        )
        self.assertEqual(str(res), EXPECTED_RESULT)
        res2 = NMEAReader.parse(res.serialize())
        self.assertEqual(str(res2), EXPECTED_RESULT)

    def testFill_GNGLL_HP(self):  # test GET constructor in high precision mode
        EXPECTED_RESULT = "<NMEA(GNGLL, lat=43.123456789, NS=N, lon=-2.987654321, EW=W, time=16:29:24.123456, status=A, posMode=A)>"
        EXPECTED_PAYLOAD = [
            "4307.4074073",
            "N",
            "00259.2592593",
            "W",
            "162924.12",
            "A",
            "A",
        ]
        res = NMEAMessage(
            "GN",
            "GLL",
            GET,
            lat=43.123456789,
            lon=-2.987654321,
            time=datetime(2023, 11, 22, 16, 29, 24, 123456).time(),
            status="A",
            posMode="A",
            hpnmeamode=1,
        )
        self.assertEqual(str(res), EXPECTED_RESULT)
        self.assertEqual(res.payload, EXPECTED_PAYLOAD)
        res2 = NMEAReader.parse(res.serialize())
        print(res.serialize())
        print(res2.serialize())

    def testFill_GNGLL_SP(self):  # test GET constructor in standard precision mode
        EXPECTED_RESULT = "<NMEA(GNGLL, lat=43.123456789, NS=N, lon=-2.987654321, EW=W, time=22:32:32, status=A, posMode=A)>"
        EXPECTED_PAYLOAD = ["4307.40741", "N", "00259.25926", "W", "223232", "A", "A"]
        res = NMEAMessage(
            "GN",
            "GLL",
            GET,
            lat=43.123456789,
            lon=-2.987654321,
            time="22:32:32",
            status="A",
            posMode="A",
            hpnmeamode=0,
        )
        self.assertEqual(str(res), EXPECTED_RESULT)
        self.assertEqual(res.payload, EXPECTED_PAYLOAD)

    def testFill_GNGLL_NSEW1(
        self,
    ):  # derive lat/lon sign from NS/EW values
        EXPECTED_RESULT = "<NMEA(GNGLL, lat=-43.123456789, NS=S, lon=-2.987654321, EW=W, time=22:32:32, status=A, posMode=A)>"
        EXPECTED_PAYLOAD = ["4307.40741", "S", "00259.25926", "W", "223232", "A", "A"]
        res = NMEAMessage(
            "GN",
            "GLL",
            GET,
            lat=-43.123456789,
            lon=-2.987654321,
            time="22:32:32",
            status="A",
            posMode="A",
            hpnmeamode=0,
        )
        self.assertEqual(str(res), EXPECTED_RESULT)
        self.assertEqual(res.payload, EXPECTED_PAYLOAD)

    def testFill_GNGLL_NSEW2(
        self,
    ):  # derive lat/lon sign from NS/EW values
        EXPECTED_RESULT = "<NMEA(GNGLL, lat=43.123456789, NS=N, lon=2.987654321, EW=E, time=22:32:32, status=A, posMode=A)>"
        EXPECTED_PAYLOAD = ["4307.40741", "N", "00259.25926", "E", "223232", "A", "A"]
        res = NMEAMessage(
            "GN",
            "GLL",
            GET,
            lat=43.123456789,
            lon=2.987654321,
            time="22:32:32",
            status="A",
            posMode="A",
            hpnmeamode=0,
        )
        self.assertEqual(str(res), EXPECTED_RESULT)
        self.assertEqual(res.payload, EXPECTED_PAYLOAD)

    def testFill_GNGLL_NSEW3(
        self,
    ):  # derive lat/lon sign from NS/EW values
        EXPECTED_RESULT = "<NMEA(GNGLL, lat=43.123456789, NS=N, lon=-2.987654321, EW=W, time=22:32:32, status=A, posMode=A)>"
        EXPECTED_PAYLOAD = ["4307.40741", "N", "00259.25926", "W", "223232", "A", "A"]
        res = NMEAMessage(
            "GN",
            "GLL",
            GET,
            lat=43.123456789,
            lon=-2.987654321,
            time="22:32:32",
            status="A",
            posMode="A",
            hpnmeamode=0,
        )
        self.assertEqual(str(res), EXPECTED_RESULT)
        self.assertEqual(res.payload, EXPECTED_PAYLOAD)

    def testFill_GRMI(
        self,
    ):  # test population ot TM and DT attributes by strings
        EXPECTED_RESULT = "<NMEA(PGRMI, lat=43.123456789, NS=N, lon=-2.987654321, EW=W, date=2025-09-18, time=22:32:32, rcvr_cmd=D)>"
        EXPECTED_PAYLOAD = [
            "4307.40741",
            "N",
            "00259.25926",
            "W",
            "180925",
            "223232",
            "D",
        ]
        res = NMEAMessage(
            "P",
            "GRMI",
            SET,
            lat=43.123456789,
            lon=-2.987654321,
            date="2025-09-18",
            time="22:32:32",
            rcvr_cmd="D",
        )
        self.assertEqual(str(res), EXPECTED_RESULT)
        self.assertEqual(res.payload, EXPECTED_PAYLOAD)

    def testFill_GNGLLUPD(self):  # test that NMEAMessage is immutable after init
        EXPECTED_ERROR = (
            "Object is immutable. Updates to lon not permitted after initialisation."
        )
        with self.assertRaises(NMEAMessageError) as context:
            res = NMEAMessage(
                "GN",
                "GLL",
                GET,
                payload=["5327.04319", "S", "00214.41396", "E", "223232.00", "A", "A"],
            )
            res.lon = 54.6666
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testFill_BADMODE(self):  # test invalid mode
        EXPECTED_ERROR = "Invalid msgmode 4 - must be 0, 1 or 2."
        with self.assertRaises(NMEAMessageError) as context:
            NMEAMessage(
                "GN",
                "GLL",
                4,
                payload=["5327.04319", "S", "00214.41396", "E", "223232.00", "A", "A"],
            )
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testFill_GNGNQ(self):  # test POLL constructor with msgId kwarg
        EXPECTED_RESULT = "<NMEA(GNGNQ, msgId=GGA)>"
        res = NMEAMessage("GN", "GNQ", POLL, msgId="GGA")
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_PUBX401(
        self,
    ):  # test SET constructor with PUBX message and payload kwarg
        EXPECTED_RESULT = "<NMEA(PUBX40, msgId=40, id=GLL, rddc=0, rus1=1, rus2=0, rusb=1, rspi=0, reserved=0)>"
        EXPECTED_PAYLOAD = b"$PUBX,40,GLL,0,1,0,1,0,0*5C\r\n"
        res = NMEAMessage(
            "P", "UBX", SET, payload=["40", "GLL", "0", "1", "0", "1", "0", "0"]
        )
        self.assertEqual(str(res), EXPECTED_RESULT)
        self.assertEqual(res.serialize(), EXPECTED_PAYLOAD)

    def testFill_PUBX402(
        self,
    ):  # test SET constructor with PUBX message and individual kwargs
        EXPECTED_RESULT = "<NMEA(PUBX40, msgId=40, id=3, rddc=0, rus1=1, rus2=0, rusb=1, rspi=0, reserved=0)>"
        EXPECTED_PAYLOAD = b"$PUBX,40,3,0,1,0,1,0,0*28\r\n"
        res = NMEAMessage("P", "UBX", SET, msgId="40", id=3, rus1=1, rusb=1)
        self.assertEqual(str(res), EXPECTED_RESULT)
        self.assertEqual(res.serialize(), EXPECTED_PAYLOAD)

    def testFill_PUBX412(
        self,
    ):  # test SET constructor with PUBX message and individual kwargs
        EXPECTED_RESULT = "<NMEA(PUBX41, msgId=41, portId=1, inProto=1, outProto=1, baudRate=115200, autobauding=0)>"
        EXPECTED_PAYLOAD = b"$PUBX,41,1,1,1,115200,0*1C\r\n"
        res = NMEAMessage(
            "P",
            "UBX",
            SET,
            msgId="41",
            portId=1,
            inProto=1,
            outProto=1,
            baudRate=115200,
            autobauding=0,
        )
        self.assertEqual(str(res), EXPECTED_RESULT)
        self.assertEqual(res.serialize(), EXPECTED_PAYLOAD)

    def testFill_PUBX4ERR(self):  # test SET constructor with missing msgId
        EXPECTED_ERROR = (
            "PUBX message definitions must include payload or msgId keyword arguments."
        )
        with self.assertRaises(NMEAMessageError) as context:
            NMEAMessage("P", "UBX", SET, id=3, rus1=1, rusb=1)
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testFill_UNKNOWN(self):  # test GET constructor with unknown msgId
        EXPECTED_ERROR = "Unknown msgID GNXXX, msgmode GET."
        with self.assertRaises(NMEAMessageError) as context:
            NMEAMessage("GN", "XXX", GET, payload=[0, 0, 0], validate=VALMSGID)
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testFill_UNKNOWN2(self):  # test GET constructor with unknown talker
        EXPECTED_ERROR = "Unknown talker XX."
        with self.assertRaises(NMEAMessageError) as context:
            NMEAMessage(
                "XX", "XXX", GET, payload=[0, 0, 0], validate=VALCKSUM | VALMSGID
            )
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testFill_UNKNOWN3(self):  # test GET constructor with unknown talker
        EXPECTED_RESULT = "<NMEA(XXXXX, NOMINAL, field_01=0, field_02=0, field_03=0)>"
        res = NMEAMessage("XX", "XXX", GET, payload=[0, 0, 0], validate=VALCKSUM)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_UNKNOWN4(self):  # test GET constructor with unknown UBX msgid
        EXPECTED_ERROR = "Unknown msgID UBX08 msgmode GET."
        with self.assertRaises(NMEAMessageError) as context:
            NMEAMessage("GN", "UBX", GET, payload=["08", 0, 0], validate=VALMSGID)
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testFill_UNKNOWN5(self):  # test GET constructor with unknown msgId
        EXPECTED_ERROR = "Unknown msgID GNXXX, msgmode GET."
        msg = NMEAMessage("GN", "XXX", GET, payload=[0, 0, 0], validate=VALCKSUM)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
