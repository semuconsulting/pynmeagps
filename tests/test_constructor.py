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

    def testGSV(self):
        EXPECTED_RESULT = "<NMEA(GPGSV, numMsg=1, msgNum=1, numSV=16, svid_01=4, elv_01=48, az_01=25, cno_01=45, svid_02=6, elv_02=78, az_02=120, cno_02=39, svid_03=18, elv_03=62, az_03=26, cno_03=52, svid_04=23, elv_04=17, az_04=99, cno_04=47, signalID=0)>"
        EXPECTED_BIN = (
            b"$GPGSV,1,1,16,4,48,25,45,6,78,120,39,18,62,26,52,23,17,99,47,0*56\r\n"
        )
        msg = NMEAMessage(
            "GP",
            "GSV",
            GET,
            numMsg=1,
            msgNum=1,
            numSV=16,
            svid_01=4,
            elv_01=48,
            az_01=25,
            cno_01=45,
            svid_02=6,
            elv_02=78,
            az_02=120,
            cno_02=39,
            svid_03=18,
            elv_03=62,
            az_03=26,
            cno_03=52,
            svid_04=23,
            elv_04=17,
            az_04=99,
            cno_04=47,
        )
        self.assertEqual(str(msg), EXPECTED_RESULT)
        self.assertEqual(msg.serialize(), EXPECTED_BIN)
        self.assertEqual(str(NMEAReader.parse(msg.serialize())), EXPECTED_RESULT)

    def testGSV2(self):
        EXPECTED_RESULT = "<NMEA(GLGSV, numMsg=1, msgNum=1, numSV=16, svid_01=4, elv_01=48, az_01=25, cno_01=45, svid_02=6, elv_02=78, az_02=120, cno_02=39, signalID=0)>"
        EXPECTED_BIN = b"$GLGSV,1,1,16,4,48,25,45,6,78,120,39,0*40\r\n"
        msg = NMEAMessage(
            "GL",
            "GSV",
            GET,
            numMsg=1,
            msgNum=1,
            numSV=16,
            svid_01=4,
            elv_01=48,
            az_01=25,
            cno_01=45,
            svid_02=6,
            elv_02=78,
            az_02=120,
            cno_02=39,
        )
        self.assertEqual(str(msg), EXPECTED_RESULT)
        self.assertEqual(msg.serialize(), EXPECTED_BIN)
        self.assertEqual(str(NMEAReader.parse(msg.serialize())), EXPECTED_RESULT)


    def testALC_empty(self):
        """ALC sentence with zero alert entries."""
        EXPECTED_STR = "<NMEA(IIALC, numSen=01, senNum=01, seqmid=00, numAlerts=0)>"
        EXPECTED_BIN = b"$IIALC,01,01,00,0*7E\r\n"
        msg = NMEAMessage(
            "II",
            "ALC",
            GET,
            numSen="01",
            senNum="01",
            seqmid="00",
            numAlerts=0,
        )
        self.assertEqual(str(msg), EXPECTED_STR)
        self.assertEqual(msg.serialize(), EXPECTED_BIN)
        # Parse round-trip: IN fields normalise to int, so zero-padding is lost
        parsed = NMEAReader.parse(msg.serialize())
        self.assertEqual(parsed.numAlerts, 0)
        self.assertEqual(parsed.seqmid, 0)

    def testALC_single_entry_null_alertinst(self):
        """ALC sentence with one alert entry, null alert instance (single-instance alert)."""
        EXPECTED_STR = "<NMEA(IIALC, numSen=01, senNum=01, seqmid=00, numAlerts=1, mfrcode_01=, alertid_01=192, alertinst_01=, revisionctr_01=3)>"
        EXPECTED_BIN = b"$IIALC,01,01,00,1,,192,,3*76\r\n"
        msg = NMEAMessage(
            "II",
            "ALC",
            GET,
            numSen="01",
            senNum="01",
            seqmid="00",
            numAlerts=1,
            mfrcode_01="",
            alertid_01="192",
            alertinst_01="",
            revisionctr_01="3",
        )
        self.assertEqual(str(msg), EXPECTED_STR)
        self.assertEqual(msg.serialize(), EXPECTED_BIN)
        parsed = NMEAReader.parse(msg.serialize())
        self.assertEqual(parsed.numAlerts, 1)
        self.assertEqual(parsed.alertid_01, "192")
        self.assertEqual(parsed.alertinst_01, "")
        self.assertEqual(parsed.revisionctr_01, "3")

    def testALC_two_entries_mixed_alertinst(self):
        """ALC sentence with two alert entries; first has a numeric alert instance,
        second has null alert instance. Verifies all four fields per entry decode
        correctly — regression test for the missing alertinst field bug."""
        EXPECTED_STR = (
            "<NMEA(IIALC, numSen=01, senNum=01, seqmid=00, numAlerts=2, "
            "mfrcode_01=, alertid_01=192, alertinst_01=1, revisionctr_01=3, "
            "mfrcode_02=XYZ, alertid_02=512, alertinst_02=, revisionctr_02=7)>"
        )
        EXPECTED_BIN = b"$IIALC,01,01,00,2,,192,1,3,XYZ,512,,7*1E\r\n"
        msg = NMEAMessage(
            "II",
            "ALC",
            GET,
            numSen="01",
            senNum="01",
            seqmid="00",
            numAlerts=2,
            mfrcode_01="",
            alertid_01="192",
            alertinst_01="1",
            revisionctr_01="3",
            mfrcode_02="XYZ",
            alertid_02="512",
            alertinst_02="",
            revisionctr_02="7",
        )
        self.assertEqual(str(msg), EXPECTED_STR)
        self.assertEqual(msg.serialize(), EXPECTED_BIN)
        parsed = NMEAReader.parse(msg.serialize())
        # Verify all four fields of entry 1
        self.assertEqual(parsed.mfrcode_01, "")
        self.assertEqual(parsed.alertid_01, "192")
        self.assertEqual(parsed.alertinst_01, "1")
        self.assertEqual(parsed.revisionctr_01, "3")
        # Verify all four fields of entry 2
        self.assertEqual(parsed.mfrcode_02, "XYZ")
        self.assertEqual(parsed.alertid_02, "512")
        self.assertEqual(parsed.alertinst_02, "")
        self.assertEqual(parsed.revisionctr_02, "7")

    def testALC_parse_wire_sentence(self):
        """Parse a raw ALC wire sentence and verify field mapping.

        Confirms that alertinst is not conflated with revisionctr — the
        defect this fix addresses (IEC 61162-1 §8.3.13, comment 4).
        """
        raw = b"$IIALC,01,01,05,1,,10001,2,3*4B\r\n"
        parsed = NMEAReader.parse(raw)
        self.assertEqual(parsed.numAlerts, 1)
        self.assertEqual(parsed.alertid_01, "10001")
        self.assertEqual(parsed.alertinst_01, "2")
        self.assertEqual(parsed.revisionctr_01, "3")

    def testALC_two_entries_mixed_alertinst(self):
        """ALC sentence with two alert entries; first has a numeric alert instance,
        second has null alert instance. Verifies all four fields per entry decode
        correctly — regression test for the missing alertinst field bug."""
        EXPECTED_RESULT = (
            "<NMEA(IIALC, numSen=01, senNum=01, seqmid=00, numAlerts=2, "
            "mfrcode_01=, alertid_01=192, alertinst_01=1, revisionctr_01=3, "
            "mfrcode_02=XYZ, alertid_02=512, alertinst_02=, revisionctr_02=7)>"
        )
        EXPECTED_BIN = b"$IIALC,01,01,00,2,,192,1,3,XYZ,512,,7*1E\r\n"
        msg = NMEAMessage(
            "II",
            "ALC",
            GET,
            numSen="01",
            senNum="01",
            seqmid="00",
            numAlerts=2,
            mfrcode_01="",
            alertid_01="192",
            alertinst_01="1",
            revisionctr_01="3",
            mfrcode_02="XYZ",
            alertid_02="512",
            alertinst_02="",
            revisionctr_02="7",
        )
        self.assertEqual(str(msg), EXPECTED_RESULT)
        self.assertEqual(msg.serialize(), EXPECTED_BIN)
        parsed = NMEAReader.parse(msg.serialize())
        # Verify all four fields of entry 1
        self.assertEqual(parsed.mfrcode_01, "")
        self.assertEqual(parsed.alertid_01, "192")
        self.assertEqual(parsed.alertinst_01, "1")
        self.assertEqual(parsed.revisionctr_01, "3")
        # Verify all four fields of entry 2
        self.assertEqual(parsed.mfrcode_02, "XYZ")
        self.assertEqual(parsed.alertid_02, "512")
        self.assertEqual(parsed.alertinst_02, "")
        self.assertEqual(parsed.revisionctr_02, "7")

    def testALC_parse_wire_sentence(self):
        """Parse a raw ALC wire sentence and verify field mapping.

        Confirms that alertinst is not conflated with revisionctr — the
        defect this fix addresses (IEC 61162-1 §8.3.13, comment 4).
        """
        raw = b"$IIALC,01,01,05,1,,10001,2,3*4B\r\n"
        parsed = NMEAReader.parse(raw)
        self.assertEqual(parsed.numAlerts, 1)
        self.assertEqual(parsed.alertid_01, "10001")
        self.assertEqual(parsed.alertinst_01, "2")
        self.assertEqual(parsed.revisionctr_01, "3")


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
