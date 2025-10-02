"""
Helper, property, static and magic method tests for pynmeagps

Created on 3 Oct 2020

*** NB: must be saved in UTF-8 format ***

:author: semuadmin (Steve Smith)
"""

import datetime
import os
import unittest

from pynmeagps import (
    NMEAMessage,
    NMEAMessageError,
    NMEAReader,
    NMEATypeError,
    NMEA_MSGIDS,
    NMEA_MSGIDS_PROP,
    NMEA_PAYLOADS_GET,
    NMEA_PAYLOADS_POLL,
    NMEA_PAYLOADS_SET,
    GPSEPOCH0,
)
from pynmeagps.nmeahelpers import (
    area,
    bearing,
    calc_checksum,
    date2str,
    date2utc,
    ddd2dmm,
    deg2dmm,
    deg2dms,
    dmm2ddd,
    dms2deg,
    ecef2llh,
    hex2str,
    generate_checksum,
    get_gpswnotow,
    get_parts,
    haversine,
    knots2spd,
    latlon2dmm,
    latlon2dms,
    llh2ecef,
    llh2iso6709,
    msgdesc,
    planar,
    time2str,
    time2utc,
    leapsecond,
)
from pynmeagps.nmeatypes_core import GET, POLL
from pynmeagps.nmeatypes_decodes import (
    GNSSLIST,
    FIXTYPE_GGA,
    FMI_STATUS,
    SIGNALID,
    SYSTEMID,
)


class StaticTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        dirname = os.path.dirname(__file__)
        self.messageCRAP = "$GNRMC,,%$£"
        self.messageBLANK = "$GNRMC,,A,,N,,W,0.046,,,,,A,V*0F"
        self.messageGLL = "$GNGLL,5327.04319,S,00214.41396,E,223232.00,A,A*68\r\n"
        self.messagePUBX = "$PUBX,00,103607.00,5327.03942,N,00214.42462,W,104.461,G3,29,31,0.085,39.63,-0.007,,5.88,7.62,8.09,6,0,0*69\r\n"
        self.messageBADCK = "$GNGLL,5327.04319,S,00214.41396,E,223232.00,A,A*22\r\n"
        self.msgGLL = NMEAReader.parse(self.messageGLL)
        self.msgPUBX00 = NMEAReader.parse(self.messagePUBX)
        self.msgGNQ = NMEAMessage("EI", "GNQ", POLL, msgId="RMC")
        self.streamNMEA2 = open(os.path.join(dirname, "pygpsdata-nmea2.log"), "rb")

    def tearDown(self):
        self.streamNMEA2.close()

    # *******************************************
    # Helper methods
    # *******************************************

    def testMissingDefs(self):  # sanity check for missing payload definitions
        for msg in NMEA_MSGIDS:
            self.assertTrue(
                msg in NMEA_PAYLOADS_GET.keys()
                or msg in NMEA_PAYLOADS_POLL
                or msg in NMEA_PAYLOADS_SET
            )

    def testMissingCodes(self):  # sanity check for missing sentence IDs
        for msg in NMEA_PAYLOADS_GET:
            self.assertTrue(msg in NMEA_MSGIDS.keys() or msg in NMEA_MSGIDS_PROP.keys())

    def testGetParts(self):
        res = get_parts(self.messageGLL)
        self.assertEqual(
            res,
            (
                "GNGLL,5327.04319,S,00214.41396,E,223232.00,A,A",
                "GN",
                "GLL",
                ["5327.04319", "S", "00214.41396", "E", "223232.00", "A", "A"],
                "68",
            ),
        )

    def testGenChecksum(self):  # test generation of new checksum
        res = generate_checksum(
            "GN", "GLL", ["5327.04319", "S", "00214.41396", "E", "223232.00", "A", "A"]
        )
        self.assertEqual(res, "68")
        res = generate_checksum(
            "GN", "GLL", ["1234.04319", "N", "00056.41396", "E", "123232.00", "A", "A"]
        )
        self.assertEqual(res, "75")

    def testGetPartsCRAP(self):  # test badly formed NMEA message
        EXPECTED_ERROR = "Badly formed message $GNRMC,,%$£"
        with self.assertRaises(NMEAMessageError) as context:
            get_parts(self.messageCRAP)
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testCalcChecksum(self):
        content, _, _, _, _ = get_parts(self.messageGLL)
        res = calc_checksum(content)
        self.assertEqual(res, "68")
        content, _, _, _, _ = get_parts(self.messagePUBX)
        res = calc_checksum(content)
        self.assertEqual(res, "69")

    def testDMM2DDD(self):
        res = dmm2ddd("5314.12345")
        self.assertEqual(res, 53.2353908333)
        res = dmm2ddd("02348.3822990")
        self.assertEqual(res, 23.80637165)
        res = dmm2ddd("00234.3822990")
        self.assertEqual(res, 2.5730383167)
        res = dmm2ddd("00214.12345")
        self.assertEqual(res, 2.2353908333)
        res = dmm2ddd("12825.12344")
        self.assertEqual(res, 128.418724)
        res = dmm2ddd("1282512344")
        self.assertEqual(res, "")
        res = dmm2ddd("2345.x5678")
        self.assertEqual(res, "")

    def testDDD2DMM(self):
        res = ddd2dmm(3.75000, "LA")
        self.assertEqual(res, "0345.00000")
        res = ddd2dmm(53.75000, "LA")
        self.assertEqual(res, "5345.00000")
        res = ddd2dmm(-2.75000, "LN")
        self.assertEqual(res, "00245.00000")
        res = ddd2dmm(128.418724, "LN")
        self.assertEqual(res, "12825.12344")
        res = ddd2dmm("", "LN")
        self.assertEqual(res, "")

    def testDDD2DMM_HPMode(self):  # high precision mode
        res = ddd2dmm(3.123456789, "LA", True)
        self.assertEqual(res, "0307.4074073")
        res = ddd2dmm(53.123456789, "LA", True)
        self.assertEqual(res, "5307.4074073")
        res = ddd2dmm(-2.123456789, "LN", True)
        self.assertEqual(res, "00207.4074073")
        res = ddd2dmm(128.123456789, "LN", True)
        self.assertEqual(res, "12807.4074073")
        res = ddd2dmm("", "LN", True)
        self.assertEqual(res, "")

    def testDMS2DEG(self):
        res = dms2deg("51°20′45.6″N")
        self.assertEqual(res, 51.346)
        self.assertEqual(deg2dms(res, "LA"), "51°20′45.6″N")
        res = dms2deg("51°30′0.0″N")
        self.assertEqual(res, 51.5)
        self.assertEqual(deg2dms(res, "LA"), "51°30′0.0″N")
        res = dms2deg("51°30.00′")
        self.assertEqual(res, 51.5)
        self.assertEqual(deg2dms(res, "LA"), "51°30′0.0″N")
        res = dms2deg("2°20′45.6″W")
        self.assertEqual(res, -2.346)
        self.assertEqual(deg2dms(res, "LN"), "2°20′45.6″W")
        res = dms2deg("33° 45′ 0.0″S")
        self.assertEqual(res, -33.75)
        self.assertEqual(deg2dms(res, "LA"), "33°45′0.0″S")
        res = dms2deg("33°45′N")
        self.assertEqual(res, 33.75)
        self.assertEqual(deg2dms(res, "LN"), "33°45′0.0″E")
        res = dms2deg("33°45.3564′N")
        self.assertEqual(res, 33.75594)
        self.assertEqual(deg2dms(res, "LA"), "33°45′21.384″N")
        res = dms2deg("28°S")
        self.assertEqual(res, -28.0)
        self.assertEqual(deg2dms(res, "LA"), "28°0′0.0″S")
        res = dms2deg("45.1234°")
        self.assertEqual(res, 45.1234)
        with self.assertRaises(ValueError) as context:
            res = dms2deg("51°°20′45.6″")
        with self.assertRaises(ValueError) as context:
            res = dms2deg("51°20′45.6″Z")
        with self.assertRaises(ValueError) as context:
            res = dms2deg("51°20′45.6″34.25`N")
        with self.assertRaises(ValueError) as context:
            res = dms2deg("xx°yy′zz.6″N")

    def testDate2UTC(self):
        res = date2utc("")
        self.assertEqual(res, "")
        res = date2utc("120320")
        self.assertEqual(res, datetime.date(2020, 3, 12))
        res = date2utc("031220", "DM")
        self.assertEqual(res, datetime.date(2020, 3, 12))
        res = date2utc("12032020", "DTL")
        self.assertEqual(res, datetime.date(2020, 3, 12))

    def testTime2UTC(self):
        res = time2utc("")
        self.assertEqual(res, "")
        res = time2utc("081123.000")
        self.assertEqual(res, datetime.time(8, 11, 23))

    def testTime2str(self):
        res = time2str(datetime.time(8, 11, 23))
        self.assertEqual(res, "081123.00")
        res = time2str("wsdfasdf")
        self.assertEqual(res, "")

    def testDate2str(self):
        res = date2str(datetime.date(2021, 3, 7))
        self.assertEqual(res, "070321")
        res = date2str(datetime.date(2021, 3, 7), "DTL")
        self.assertEqual(res, "07032021")
        res = date2str(datetime.date(2021, 3, 7), "DM")
        self.assertEqual(res, "030721")
        res = date2str("wsdfasdf")
        self.assertEqual(res, "")

    def testKnots2spd(self):
        res = knots2spd(1.0, "MS")
        self.assertAlmostEqual(res, 0.5144447324, 5)
        res = knots2spd(1.0, "FS")
        self.assertAlmostEqual(res, 1.68781084, 5)
        res = knots2spd(1.0, "mph")
        self.assertAlmostEqual(res, 1.15078, 5)
        res = knots2spd(1.0, "kmph")
        self.assertAlmostEqual(res, 1.852001, 5)

    def testKnots2spdBAD(self):
        EXPECTED_ERROR = (
            "Invalid conversion unit CRAP - must be in ['MS', 'FS', 'MPH', 'KMPH']."
        )
        with self.assertRaises(KeyError) as context:
            knots2spd(1.0, "CRAP")
        self.assertTrue(EXPECTED_ERROR in str(context.exception))
        EXPECTED_ERROR = "Invalid knots value CRAP - must be float or integer."
        with self.assertRaises(TypeError) as context:
            knots2spd("CRAP", "MS")
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testMsgDesc(self):
        res = msgdesc("GGA")
        self.assertEqual(res, "Global positioning system fix data")
        res = msgdesc("UBX03")
        self.assertEqual(res, "Satellite Status")
        res = msgdesc("XXX")
        self.assertEqual(res, "Unknown msgID XXX")

    # *******************************************
    # NMEAMessage property methods
    # *******************************************

    def testIdentity(self):
        res = self.msgGLL.identity
        self.assertEqual(res, "GNGLL")

    def testTalkerS(self):
        res = self.msgGLL.talker
        self.assertEqual(res, "GN")

    def testTalkerP(self):
        res = self.msgPUBX00.talker
        self.assertEqual(res, "P")

    def testMsgIDS(self):
        res = self.msgGLL.msgID
        self.assertEqual(res, "GLL")

    def testMsgIDP(self):
        res = self.msgPUBX00.msgID
        self.assertEqual(res, "UBX")

    def testMsgmode0(self):
        res = self.msgGLL.msgmode
        self.assertEqual(res, GET)

    def testMsgmode2(self):
        res = self.msgGNQ.msgmode
        self.assertEqual(res, POLL)

    def testdatastream(self):  # test datastream getter
        EXPECTED_RESULT = "<class '_io.BufferedReader'>"
        res = str(type(NMEAReader(self.streamNMEA2).datastream))
        self.assertEqual(res, EXPECTED_RESULT)

    def testPayloadS(self):
        res = self.msgGLL.payload
        self.assertEqual(
            res, ["5327.04319", "S", "00214.41396", "E", "223232.00", "A", "A"]
        )

    def testPayloadP(self):
        res = self.msgPUBX00.payload
        self.assertEqual(
            res,
            [
                "00",
                "103607.00",
                "5327.03942",
                "N",
                "00214.42462",
                "W",
                "104.461",
                "G3",
                "29",
                "31",
                "0.085",
                "39.63",
                "-0.007",
                "",
                "5.88",
                "7.62",
                "8.09",
                "6",
                "0",
                "0",
            ],
        )

    def testChecksumS(self):
        res = self.msgGLL.checksum
        self.assertEqual(res, "68")

    def testChecksumP(self):
        res = self.msgPUBX00.checksum
        self.assertEqual(res, "69")

    # *******************************************
    # NMEAMessage static methods
    # *******************************************

    def testSerializeS(self):
        res = self.msgGLL.serialize()
        self.assertEqual(res, b"$GNGLL,5327.04319,S,00214.41396,E,223232.00,A,A*68\r\n")

    def testSerializeP(self):
        res = self.msgPUBX00.serialize()
        self.assertEqual(
            res,
            b"$PUBX,00,103607.00,5327.03942,N,00214.42462,W,104.461,G3,29,31,0.085,39.63,-0.007,,5.88,7.62,8.09,6,0,0*69\r\n",
        )

    def testStrS(
        self,
    ):  # double check that parsing of serialized message reproduces original message
        res1 = self.msgGLL
        res2 = NMEAReader.parse(self.msgGLL.serialize())
        self.assertEqual(str(res1), str(res2))

    def testStrP(self):
        res1 = self.msgPUBX00
        res2 = NMEAReader.parse(self.msgPUBX00.serialize())
        self.assertEqual(str(res1), str(res2))

    def testNomVal(self):
        for att in ("CH", "ST", "LA", "LN"):
            res = NMEAMessage.nomval(att)
            self.assertEqual(res, "")
        res = NMEAMessage.nomval("HX")
        self.assertEqual(res, "0")
        res = NMEAMessage.nomval("IN")
        self.assertEqual(res, 0)
        res = NMEAMessage.nomval("DE")
        self.assertEqual(res, 0.0)
        res = NMEAMessage.nomval("TM")
        self.assertIsInstance(res, datetime.time)
        res = NMEAMessage.nomval("DT")
        self.assertIsInstance(res, datetime.date)

    def testNomValBAD(self):
        EXPECTED_ERROR = "Unknown attribute type XX."
        with self.assertRaises(NMEATypeError) as context:
            NMEAMessage.nomval("XX")
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testVal2Str(self):
        for att in ("CH", "ST"):
            res = NMEAMessage.val2str("AB", att)
            self.assertEqual(res, "AB")
        res = NMEAMessage.val2str("B", "HX")
        self.assertEqual(res, "B")
        res = NMEAMessage.val2str(23, "IN")
        self.assertEqual(res, "23")
        res = NMEAMessage.val2str(15.286, "DE")
        self.assertEqual(res, "15.286")
        res = NMEAMessage.val2str(55.5, "LA")
        self.assertEqual(res, "5530.00000")
        res = NMEAMessage.val2str(2.75, "LN")
        self.assertEqual(res, "00245.00000")
        res = NMEAMessage.val2str(datetime.datetime(2021, 5, 7, 2, 45, 23), "TM")
        self.assertEqual(res, "024523.00")
        res = NMEAMessage.val2str(datetime.datetime(2020, 6, 7, 3, 27, 24), "DT")
        self.assertEqual(res, "070620")

    def testVal2StrBAD(self):
        EXPECTED_ERROR = "Unknown attribute type XX."
        with self.assertRaises(NMEATypeError) as context:
            NMEAMessage.val2str(23.45, "XX")
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    # *******************************************
    # NMEAMessage magic methods
    # *******************************************

    def testReprS(self):
        res = repr(self.msgGLL)
        self.assertEqual(
            res,
            "NMEAMessage('GN','GLL', 0, payload=['5327.04319', 'S', '00214.41396', 'E', '223232.00', 'A', 'A'])",
        )

    def testReprP(self):
        res = repr(self.msgPUBX00)
        self.assertEqual(
            res,
            "NMEAMessage('P','UBX', 0, payload=['00', '103607.00', '5327.03942', 'N', '00214.42462', 'W', '104.461', 'G3', '29', '31', '0.085', '39.63', '-0.007', '', '5.88', '7.62', '8.09', '6', '0', '0'])",
        )

    def testEvalReprS(
        self,
    ):  # double check that evaluation of repr(message) reproduces original message
        res1 = self.msgGLL
        res2 = eval(repr(self.msgGLL))
        self.assertEqual(str(res1), str(res2))

    def testEvalReprP(self):
        res1 = self.msgPUBX00
        res2 = eval(repr(self.msgPUBX00))
        self.assertEqual(str(res1), str(res2))

    # *******************************************
    # NMEAMessage helpers
    # *******************************************

    def testdeg2dms(self):
        res = deg2dms(53.346, "LA")
        self.assertEqual(res, ("53°20′45.6″N"))
        res = deg2dms("xxx", "LA")
        self.assertEqual(res, "")

    def testdeg2dmm(self):
        res = deg2dmm(-2.5463, "LN")
        self.assertEqual(res, ("2°32.778′W"))
        res = deg2dmm("xxx", "LN")
        self.assertEqual(res, "")

    def testlatlon2dms(self):
        res = latlon2dms(53.346, -2.5463)
        self.assertEqual(res, ("53°20′45.6″N", "2°32′46.68″W"))

    def testlatlon2dmm(self):
        res = latlon2dmm(53.346, -2.5463)
        self.assertEqual(res, ("53°20.76′N", "2°32.778′W"))

    def testlatlon2dmm(self):
        res = latlon2dmm(53.346, -2.5463)
        self.assertEqual(res, ("53°20.76′N", "2°32.778′W"))

    def testllh2iso6709(self):
        res = llh2iso6709(53.12, -2.165, 35)
        self.assertEqual(res, "+53.12-2.165+35CRSWGS_84/")
        res = llh2iso6709(-53.12, +2.165, 68.45)
        self.assertEqual(res, "-53.12+2.165+68.45CRSWGS_84/")

    def testecef2llh(self):
        vals = [
            (3822566.3113, -144427.5123, 5086857.1208),
            (3980570.0700029507, 0.0, 4966833.391498124),
            (10000, 10000, 10000),
        ]
        res = [
            (53.24168283407136, -2.1637695489854565, 214.9785466667861),
            (51.4779280000001, 0, 5.8584775974986524e-09),
            (0, 0, -1.0e7),
        ]
        for i, val in enumerate(vals):
            lat, lon, alt = ecef2llh(val[0], val[1], val[2])
            self.assertAlmostEqual(lat, res[i][0], 5)
            self.assertAlmostEqual(lon, res[i][1], 5)
            self.assertAlmostEqual(alt, res[i][2], 5)

    def testllh2ecef(self):
        vals = [
            (53.24168283407126, -2.1637695489854565, 214.97854665775156),
            (51.477928, 0, 0),
        ]
        res = [
            (3822566.311300003, -144427.51230000015, 5086857.120799987),
            (3980570.0700029545, 0.0, 4966833.3914981127),
        ]
        for i, val in enumerate(vals):
            x, y, z = llh2ecef(val[0], val[1], val[2])
            self.assertAlmostEqual(x, res[i][0], 5)
            self.assertAlmostEqual(y, res[i][1], 5)
            self.assertAlmostEqual(z, res[i][2], 5)

    def testllh2eceftab(self):  # test conversion there and back
        vals = [
            (53.24, -2.16, 214.98),
            (-7.48, 67.87, 43.12),
            (-34.51, -56.09, 1745.98),
            (90, 90, -435184.65),
            (0, 0, 0),
        ]
        for i, val in enumerate(vals):
            x, y, z = llh2ecef(val[0], val[1], val[2])
            lat, lon, alt = ecef2llh(x, y, z)
            self.assertAlmostEqual(lat, val[0], 2)
            self.assertAlmostEqual(lon, val[1], 2)
            self.assertAlmostEqual(alt, val[2], 2)

    def testhaversine(self):
        res = haversine(51.23, -2.41, 34.205, 56.34)
        self.assertAlmostEqual(res, 5010.722, 3)
        res = haversine(-12.645, 34.867, 145.1745, -56.27846)
        self.assertAlmostEqual(res, 10715.371, 3)
        res = haversine(53.45, -2.14, 53.451, -2.141)
        self.assertAlmostEqual(res, 0.1296, 3)

    def testplanar(self):  # test planar
        res = planar(53, 2, 53.000001, 2.000001)
        # print(res)
        self.assertAlmostEqual(res, 0.12992378701316823, 7)
        res = planar(53, 2, 53.00001, 2.00001)
        # print(res)
        self.assertAlmostEqual(res, 1.299237873027932, 7)
        res = planar(53, 2, 53.0001, 2.0001)
        # print(res)
        self.assertAlmostEqual(res, 12.992378723687828, 7)

    def testbearing(self):
        res = bearing(51.23, -2.41, 53.205, -2.34)
        self.assertAlmostEqual(res, 1.216362703824359, 4)
        res = bearing(51.23145, -2.41, 51.23145, -2.34)
        self.assertAlmostEqual(res, 89.9727111358776, 4)
        res = bearing(51.23, -2.41, 34.205, 56.34)
        self.assertAlmostEqual(res, 88.58134073451902, 4)
        res = bearing(-12.645, 34.867, -34.1745, 48.27846)
        self.assertAlmostEqual(res, 152.70835788275326, 4)

    def testarea(self):
        res = area(51.23, -2.41, 53.205, -2.34)
        self.assertAlmostEqual(res, 1049.5657, 4)
        res = area(53.48280729, -2.24225376, 53.46814647, -2.20192543)
        self.assertAlmostEqual(res, 4.3606, 4)
        res = area(53.69865772, -2.68269539, 53.22939103, -1.39218885)
        self.assertAlmostEqual(res, 4467.6282, 4)
        res = area(-12.645, 34.867, -34.1745, 48.27846)
        self.assertAlmostEqual(res, 3264291.8230, 4)

    def testgpsweek(self):
        dats = [
            (2023, 1, 1),
            (2005, 11, 5),
            (2020, 8, 20),
            (2014, 3, 16),
            (2023, 5, 21),
            (2023, 5, 27),
        ]
        vals = [
            (2243, 0),
            (1347, 518400),
            (2119, 345600),
            (1784, 0),
            (2263, 0),
            (2263, 518400),
        ]
        for i, dat in enumerate(dats):
            y, m, d = dat
            self.assertEqual(get_gpswnotow(datetime.datetime(y, m, d)), vals[i])

    def testhex2str(self):
        hex = 0x1234ABCD
        self.assertEqual(hex2str(hex, 8), "1234ABCD")
        hex = 0x123B
        self.assertEqual(hex2str(hex, 8), "0000123B")
        self.assertEqual(hex2str(hex, 6), "00123B")
        self.assertEqual(hex2str(hex), "123B")

    def testdecodes(self):

        self.assertEqual(GNSSLIST[0], "GPS")
        self.assertEqual(FIXTYPE_GGA[1], "2D")
        self.assertEqual(FMI_STATUS[2], ("Ready", "Filter convergence completion flag"))
        self.assertEqual(SIGNALID[("1", "5")], "GPS L2 CM")
        self.assertEqual(SYSTEMID["4"], "Beidou")

    def testleapsecond(self):
        self.assertEqual(leapsecond(GPSEPOCH0), 0)
        self.assertEqual(leapsecond(datetime.datetime(1985, 1, 1, 0, 0, 0)), 3)
        self.assertEqual(leapsecond(datetime.datetime(1997, 8, 1, 0, 0, 0)), 12)
        self.assertEqual(leapsecond(datetime.datetime(2025, 9, 18, 16, 51, 34)), 18)
        self.assertEqual(leapsecond(datetime.datetime(1974, 9, 18, 16, 51, 34)), -6)
        self.assertEqual(leapsecond(datetime.datetime(1971, 9, 18, 16, 51, 34)), 0)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
