'''
Constructor method tests for pynmeagps

Created on 4 Mar 2021

*** NB: must be saved in UTF-8 format ***

:author: semuadmin
'''

import unittest

from pynmeagps import NMEAMessage, GET, SET, POLL, NMEAMessageError


class FillTest(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def testFill_GNGLL(self):  # test GET constructor with full payload keyword
        EXPECTED_RESULT = "<NMEA(GNGLL, lat=-53.45072, NS=S, lon=2.240233, EW=E, time=22:32:32, status=A, posMode=A)>"
        res = NMEAMessage('GN', 'GLL', GET, payload=['5327.04319', 'S', '00214.41396', 'E', '223232.00', 'A', 'A'])
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_GNGLLUPD(self):  # test that NMEAMessage is immutable after init
        EXPECTED_ERROR = "Object is immutable. Updates to lon not permitted after initialisation."
        with self.assertRaises(NMEAMessageError) as context:
            res = NMEAMessage('GN', 'GLL', GET, payload=['5327.04319', 'S', '00214.41396', 'E', '223232.00', 'A', 'A'])
            res.lon = 54.6666
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testFill_BADMODE(self):  # test invalid mode
        EXPECTED_ERROR = "Invalid mode 4 - must be 0, 1 or 2."
        with self.assertRaises(NMEAMessageError) as context:
            NMEAMessage('GN', 'GLL', 4, payload=['5327.04319', 'S', '00214.41396', 'E', '223232.00', 'A', 'A'])
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testFill_GNGNQ(self):  # test POLL constructor with msgId kwarg
        EXPECTED_RESULT = "<NMEA(GNGNQ, msgId=GGA)>"
        res = NMEAMessage('GN', 'GNQ', POLL, msgId='GGA')
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_PUBX401(self):  # test SET constructor with PUBX message and payload kwarg
        EXPECTED_RESULT = "<NMEA(PUBX, msgId=40, id=2, rddc=0, rus1=1, rus2=0, rusb=1, rspi=0, reserved=0)>"
        res = NMEAMessage('', 'PUBX', SET, payload=['40', '02', '0', '1', '0', '1', '0', '0'])
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_PUBX402(self):  # test SET constructor with PUBX message and individual kwargs
        EXPECTED_RESULT = "<NMEA(PUBX, msgId=40, id=3, rddc=0, rus1=1, rus2=0, rusb=1, rspi=0, reserved=0)>"
        res = NMEAMessage('', 'PUBX', SET, msgId='40', id=3, rus1=1, rusb=1)
        self.assertEqual(str(res), EXPECTED_RESULT)

    def testFill_PUBX4ERR(self):  # test SET constructor with missing msgId
        EXPECTED_ERROR = "PUBX message definitions must include payload or msgId keyword arguments."
        with self.assertRaises(NMEAMessageError) as context:
            NMEAMessage('', 'PUBX', SET, id=3, rus1=1, rusb=1)
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testFill_UNKNOWN(self):  # test GET constructor with unknown msgId
        EXPECTED_ERROR = "Unknown message type msgID XXX msgmode GET."
        with self.assertRaises(NMEAMessageError) as context:
            NMEAMessage('GN', 'XXX', GET, payload=[0, 0, 0])
        self.assertTrue(EXPECTED_ERROR in str(context.exception))


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
