'''
Helper, property, static and magic method tests for pynmeagps

Created on 3 Oct 2020

*** NB: must be saved in UTF-8 format ***

:author: semuadmin
'''

import unittest
import datetime
from pynmeagps import NMEAReader, NMEAMessage, NMEAMessageError  # pylint: disable=unused-import
import pynmeagps.nmeahelpers as nmh


class StaticTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.messageCRAP = '$GNRMC,,%$£'
        self.messageBLANK = '$GNRMC,,A,,N,,W,0.046,,,,,A,V*0F'
        self.messageGLL = '$GNGLL,5327.04319,S,00214.41396,E,223232.00,A,A*68\r\n'
        self.messagePUBX = '$PUBX,00,103607.00,5327.03942,N,00214.42462,W,104.461,G3,29,31,0.085,39.63,-0.007,,5.88,7.62,8.09,6,0,0*69\r\n'
        self.messageBADCK = '$GNGLL,5327.04319,S,00214.41396,E,223232.00,A,A*22\r\n'
        self.msgGLL = NMEAReader.parse(self.messageGLL, True)
        self.msgPUBX00 = NMEAReader.parse(self.messagePUBX, True)

    def tearDown(self):
        pass

#*******************************************
# Helper methods
#*******************************************

    def testInt2Hex(self):
        res = nmh.int2hexstr(15)
        self.assertEqual(res, '0F')
        res = nmh.int2hexstr(104)
        self.assertEqual(res, '68')

    def testGetParts(self):
        res = nmh.get_parts(self.messageGLL)
        self.assertEqual(res, ('GN', 'GLL', ['5327.04319', 'S', '00214.41396', 'E', '223232.00', 'A', 'A'], '68'))

    def testGetPartsCRAP(self):  # test badly formed NMEA message
        EXPECTED_ERROR = "Badly formed message $GNRMC,,%$£"
        with self.assertRaises(NMEAMessageError) as context:
            nmh.get_parts(self.messageCRAP)
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testGetContent(self):
        res = nmh.get_content(self.messageGLL)
        self.assertEqual(res, 'GNGLL,5327.04319,S,00214.41396,E,223232.00,A,A')

    def testCalcChecksum(self):
        res = nmh.calc_checksum(self.messageGLL)
        self.assertEqual(res, '68')
        res = nmh.calc_checksum(self.messagePUBX)
        self.assertEqual(res, '69')

    def testGoodChecksum(self):
        res = nmh.isvalid_cksum(self.messageGLL)
        self.assertEqual(res, True)

    def testBadChecksum(self):
        res = nmh.isvalid_cksum(self.messageBADCK)
        self.assertEqual(res, False)

    def testDMM2DDD(self):
        res = nmh.dmm2ddd('5314.12345', 'LA')
        self.assertEqual(res, 53.235391)
        res = nmh.dmm2ddd('00214.12345', 'LN')
        self.assertEqual(res, 2.235391)

    def testDate2UTC(self):
        res = nmh.date2utc('')
        self.assertEqual(res, "")
        res = nmh.date2utc('120320')
        self.assertEqual(res, datetime.date(2020, 3, 12))

    def testTime2UTC(self):
        res = nmh.time2utc('')
        self.assertEqual(res, "")
        res = nmh.time2utc('081123.000')
        self.assertEqual(res, datetime.time(8, 11, 23))

#*******************************************
# NMEAMessage property methods
#*******************************************

    def testTalkerS(self):
        res = self.msgGLL.talker
        self.assertEqual(res, 'GN')

    def testTalkerP(self):
        res = self.msgPUBX00.talker
        self.assertEqual(res, '')

    def testMsgIDS(self):
        res = self.msgGLL.msgID
        self.assertEqual(res, 'GLL')

    def testMsgIDP(self):
        res = self.msgPUBX00.msgID
        self.assertEqual(res, 'PUBX')

    def testPayloadS(self):
        res = self.msgGLL.payload
        self.assertEqual(res, ['5327.04319', 'S', '00214.41396', 'E', '223232.00', 'A', 'A'])

    def testPayloadP(self):
        res = self.msgPUBX00.payload
        self.assertEqual(res, ['00', '103607.00', '5327.03942', 'N', '00214.42462', 'W', '104.461', 'G3', '29', '31', '0.085', '39.63', '-0.007', '', '5.88', '7.62', '8.09', '6', '0', '0'])

    def testChecksumS(self):
        res = self.msgGLL.checksum
        self.assertEqual(res, '68')

    def testChecksumP(self):
        res = self.msgPUBX00.checksum
        self.assertEqual(res, '69')

#*******************************************
# NMEAMessage static methods
#*******************************************

    def testSerializeS(self):
        res = self.msgGLL.serialize()
        self.assertEqual(res, b'$GNGLL,5327.04319,S,00214.41396,E,223232.00,A,A*68\r\n')

    def testSerializeP(self):
        res = self.msgPUBX00.serialize()
        self.assertEqual(res, b'$PUBX,00,103607.00,5327.03942,N,00214.42462,W,104.461,G3,29,31,0.085,39.63,-0.007,,5.88,7.62,8.09,6,0,0*69\r\n')

    def testStrS(self):  # double check that parsing of serialized message reproduces original message
        res1 = self.msgGLL
        res2 = NMEAReader.parse(self.msgGLL.serialize())
        self.assertEqual(str(res1), str(res2))

    def testStrP(self):
        res1 = self.msgPUBX00
        res2 = NMEAReader.parse(self.msgPUBX00.serialize())
        self.assertEqual(str(res1), str(res2))

#*******************************************
# NMEAMessage magic methods
#*******************************************

    def testReprS(self):
        res = repr(self.msgGLL)
        self.assertEqual(res, "NMEAMessage('GN','GLL', 0, payload=['5327.04319', 'S', '00214.41396', 'E', '223232.00', 'A', 'A'])")

    def testReprP(self):
        res = repr(self.msgPUBX00)
        self.assertEqual(res, "NMEAMessage('','PUBX', 0, payload=['00', '103607.00', '5327.03942', 'N', '00214.42462', 'W', '104.461', 'G3', '29', '31', '0.085', '39.63', '-0.007', '', '5.88', '7.62', '8.09', '6', '0', '0'])")

    def testEvalReprS(self):  # double check that evaluation of repr(message) reproduces original message
        res1 = self.msgGLL
        res2 = eval(repr(self.msgGLL))
        self.assertEqual(str(res1), str(res2))

    def testEvalReprP(self):
        res1 = self.msgPUBX00
        res2 = eval(repr(self.msgPUBX00))
        self.assertEqual(str(res1), str(res2))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
