'''
Exception handling tests for pynmeagps

Created on 4 Mar 2021

*** NB: must be saved in UTF-8 format ***

:author: semuadmin
'''

import unittest

from pynmeagps import NMEAMessage, NMEAReader, NMEATypeError, NMEAParseError, NMEAMessageError, NMEAStreamError, GET, SET, POLL


class ExceptionTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
