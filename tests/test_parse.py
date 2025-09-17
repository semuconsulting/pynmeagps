"""
Parse method tests for pynmeagps
(most parse() functionality tested in test_stream.py)

Created on 4 Mar 2021

*** NB: must be saved in UTF-8 format ***

:author: semuadmin (Steve Smith)
"""

import unittest
from pynmeagps import (
    NMEAReader,
    NMEAMessageError,
    NMEAParseError,
    ERR_RAISE,
    SET,
    VALCKSUM,
    VALMSGID,
)


class ParseTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.messageGLL = "$GNGLL,5327.04319,S,00214.41396,E,223232.00,A,A*68\r\n"
        self.messageGLL_HP = (
            "$GNGLL,5327.0431923,S,00214.4139641,E,223232.00,A,A*6C\r\n"
        )
        self.messagePKLSH = "$PKLSH,3851.3330,N,09447.9417,W,012212,V,100,1202,*24\r\n"
        self.messagePUBX = "$PUBX,00,103607.00,5327.03942,N,00214.42462,W,104.461,G3,29,31,0.085,39.63,-0.007,,5.88,7.62,8.09,6,0,0*69\r\n"
        self.messagePGRMM = "$PGRMM,WGS84*26\r\n"
        self.messagePGRMO = "$PGRMO,PGRMM,2*30\r\n"
        self.messageNK = "$GNXXX,5327.04319,S,00214.41396,E,223232.00,A,A*77\r\n"
        self.messageBADCK = "$GNGLL,5327.04319,S,00214.41396,E,223232.00,A,A*22\r\n"

    def tearDown(self):
        pass

    def testParseGLL(self):  # standard message
        res = NMEAReader.parse(self.messageGLL)
        self.assertEqual(
            str(res),
            (
                "<NMEA(GNGLL, lat=-53.4507198333, NS=S, lon=2.2402326667, EW=E, time=22:32:32, status=A, posMode=A)>"
            ),
        )

    def testParseGLL_HPMODE(self):  # standard message, HP mode
        res = NMEAReader.parse(self.messageGLL_HP)
        self.assertEqual(
            str(res),
            (
                "<NMEA(GNGLL, lat=-53.4507198717, NS=S, lon=2.240232735, EW=E, time=22:32:32, status=A, posMode=A)>"
            ),
        )
        print(res.serialize())

    def testParsePKLSH(self):  # Proprietary JVCKenwood message
        res = NMEAReader.parse(self.messagePKLSH)
        self.assertEqual(
            str(res),
            "<NMEA(PKLSH, lat=38.85555, NS=N, lon=-94.7990283333, EW=W, time=01:22:12, status=V, fleetId=100, deviceId=1202)>",
        )

    def testParsePUBX(self):  # proprietary UBX message
        res = NMEAReader.parse(self.messagePUBX)
        self.assertEqual(
            str(res),
            (
                "<NMEA(PUBX00, msgId=00, time=10:36:07, lat=53.450657, NS=N, lon=-2.2404103333, EW=W, altRef=104.461, navStat=G3, hAcc=29.0, vAcc=31.0, SOG=0.085, COG=39.63, vVel=-0.007, diffAge=, HDOP=5.88, VDOP=7.62, TDOP=8.09, numSVs=6, reserved=0, DR=0)>"
            ),
        )

    def testParsePGRMM(self):  # proprietary GARMIN message
        res = NMEAReader.parse(self.messagePGRMM)
        self.assertEqual(str(res), ("<NMEA(PGRMM, dtm=WGS84)>"))

    def testParsePGRMO(self):  # parse SET message
        res = NMEAReader.parse(self.messagePGRMO, msgmode=SET)
        self.assertEqual(str(res), ("<NMEA(PGRMO, msgId=PGRMM, tgtmode=2)>"))

    def testParseNK(
        self,
    ):  # unknown message identifier with validate (VALCKSUM + VALMSGID) - should be rejected
        EXPECTED_ERROR = "Unknown msgID GNXXX, msgmode GET."
        with self.assertRaises(NMEAParseError) as context:
            NMEAReader.parse(self.messageNK, validate=VALCKSUM | VALMSGID)
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testParseNK2(
        self,
    ):  # unknown message identifier with validate VALCKSUM only - should just be ignored.
        EXPECTED_RESULT = "<NMEA(GNXXX, NOMINAL, field_01=5327.04319, field_02=S, field_03=00214.41396, field_04=E, field_05=223232.00, field_06=A, field_07=A)>"
        res = NMEAReader.parse(self.messageNK, validate=VALCKSUM)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testParseBADMODE(self):  # invalid mode setting
        EXPECTED_ERROR = "Invalid parse mode 4 - must be 0, 1 or 2."
        with self.assertRaises(NMEAParseError) as context:
            NMEAReader.parse(self.messageGLL, msgmode=4)
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testParseBADCK(self):  # invalid checksum
        EXPECTED_ERROR = "Message GNGLL invalid checksum 22 - should be 68."
        with self.assertRaises(NMEAParseError) as context:
            NMEAReader.parse(self.messageBADCK)
        self.assertTrue(EXPECTED_ERROR in str(context.exception))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
