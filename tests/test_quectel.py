"""
Quectel LG290P Stream method tests for pynmeagps

Created on 19 Aug 2024

*** NB: must be saved in UTF-8 format ***

:author: semuadmin
"""

import os
import sys
import unittest

from pynmeagps import (
    NMEAReader,
    NMEAMessage,
    VALCKSUM,
    VALMSGID,
    SET,
    GET,
    POLL,
    hex2str,
)

DIRNAME = os.path.dirname(__file__)


class QuectelStreamTest(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

    def catchio(self):
        """
        Capture stdout as string.
        """

        self._saved_stdout = sys.stdout
        self._strout = os.StringIO()
        sys.stdout = self._strout

    def restoreio(self) -> str:
        """
        Return captured output and restore stdout.
        """

        sys.stdout = self._saved_stdout
        return self._strout.getvalue().strip()

    def testNMEAQUECTELGET(self):  # test proprietary Quectel LG290P GET messages
        EXPECTED_RESULTS = (
            "<NMEA(PQTMVER, msgver=1, vername=MODULE, verstr=LG290P03AANR01A03S, builddate=2024/04/30, buildtime=10:53:07)>",
            "<NMEA(PQTMVERNO, verstr=LG290P03AANR01A03S, builddate=2024/04/30, buildtime=10:53:07)>",
            "<NMEA(PQTMEPE, msgver=2, epenorth=1.0, epeeast=1.0, epedown=1.0, epe2d=1.414, epe3d=1.732)>",
            "<NMEA(PQTMVEL, msgver=1, time=15:45:12.100000, veln=1.251, vele=2.452, veld=1.245, gndspd=2.752, spd=3.021, hdg=180.512, gndspdacc=0.124, spdacc=0.254, hdgacc=0.25)>",
            "<NMEA(PQTMGEOFENCESTATUS, msgver=1, time=12:45:21, staten_01=1, staten_02=2, staten_03=2, staten_04=2)>",
            "<NMEA(PQTMTXT, msgver=1, totalsennum=1, sennum=1, textid=1, text=0x105f0cf810417c00)>",
            "<NMEA(PQTMSVINSTATUS, msgver=1, tow=1000, valid=1, reserved0=, reserved1=1, obs=20, cfgdur=100, meanx=-2484434.3645, meany=4875976.9741, meanz=3266161.3412, meanacc=1.2415)>",
            "<NMEA(PQTMPVT, msgver=1, tow=1000, date=20221225, time=16:33:55, reserved=, fixtype=0, numsv=0, leaps=, lat=, lon=, alt=, sep=, veln=, vele=, veld=, spd=, hdg=, hdop=99.99, pdop=99.99)>",
            "<NMEA(PQTMPVT, msgver=1, tow=31075000, date=20221225, time=08:37:37, reserved=, fixtype=3, numsv=9, leaps=18, lat=31.12738291, lon=117.2637291, alt=34.212, sep=5.267, veln=3.212, vele=2.928, veld=0.238, spd=4.346, hdg=34.12, hdop=2.16, pdop=4.38)>",
            "<NMEA(PQTMDOP, msgver=1, tow=570643000, gdop=1.01, pdop=0.88, tdop=0.49, vdop=0.73, hdop=0.5, ndop=0.36, edop=0.35)>",
            "<NMEA(PQTMDOP, msgver=1, tow=, gdop=99.99, pdop=99.99, tdop=99.99, vdop=99.99, hdop=99.99, ndop=99.99, edop=99.99)>",
            "<NMEA(PQTMPL, msgver=1, tow=55045200, pul=5.0, reserved1=1, reserved2=1, plposn=2879.0, plpose=2718.0, plposd=4766.0, plveln=5344.0, plvele=4323.0, plveld=10902.0, reserved3=, reserved4=, pltime=)>",
            "<NMEA(PQTMODO, msgver=1, time=12:06:35, state=1, dist=112.3)>",
        )
        i = 0
        raw = 0
        with open(os.path.join(DIRNAME, "quectel_nmea_get.log"), "rb") as stream:
            nmr = NMEAReader(
                stream, validate=VALCKSUM | VALMSGID, quitonerror=2, msgmode=GET
            )
            for raw, parsed in nmr:
                if raw is not None:
                    # print(f'"{parsed}",')
                    self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                    i += 1
        self.assertEqual(i, len(EXPECTED_RESULTS))

    def testNMEAQUECTELPOLL(self):  # test proprietary Quectel LG290P POLL messages
        EXPECTED_RESULTS = (
            "<NMEA(PQTMCFGUART, status=R)>",
            "<NMEA(PQTMCFGUART, status=R, portid=1)>",
            "<NMEA(PQTMCFGPPS, status=R, ppsindex=1)>",
            "<NMEA(PQTMCFGPROT, status=R, porttype=1, portid=1)>",
            "<NMEA(PQTMCFGNMEADP, status=R)>",
            "<NMEA(PQTMCFGMSGRATE, status=R, msgname=GGA)>",
            "<NMEA(PQTMCFGMSGRATE, status=R, msgname=PQTMEPE, msgver=2)>",
            "<NMEA(PQTMCFGMSGRATE, status=R, msgname=RTCM3-1005)>",
            "<NMEA(PQTMCFGMSGRATE, status=R, msgname=RTCM3-107X)>",
            "<NMEA(PQTMCFGMSGRATE, status=R, msgname=RTCM3-1019)>",
            "<NMEA(PQTMCFGGEOFENCE, status=R, geofenceindex=0)>",
            "<NMEA(PQTMCFGSVIN, status=R)>",
            "<NMEA(PQTMCFGRCVRMODE, status=R)>",
            "<NMEA(PQTMCFGFIXRATE, status=R)>",
            "<NMEA(PQTMCFGRTK, status=R)>",
            "<NMEA(PQTMCFGCNST, status=R)>",
            "<NMEA(PQTMCFGODO, status=R)>",
            "<NMEA(PQTMCFGSIGNAL, status=R)>",
            "<NMEA(PQTMCFGSAT, status=R, systemid=1, signalid=1)>",
            "<NMEA(PQTMCFGSAT, status=R, systemid=4, signalid=1)>",
            "<NMEA(PQTMCFGRSID, status=R)>",
        )
        i = 0
        raw = 0
        with open(os.path.join(DIRNAME, "quectel_nmea_poll.log"), "rb") as stream:
            nmr = NMEAReader(
                stream, validate=VALCKSUM | VALMSGID, quitonerror=2, msgmode=POLL
            )
            for raw, parsed in nmr:
                if raw is not None:
                    # print(f'"{parsed}",')
                    self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                    i += 1
        self.assertEqual(i, len(EXPECTED_RESULTS))

    def testNMEAQUECTELCOMMAND(
        self,
    ):  # test proprietary Quectel LG290P Command (SET) messages
        EXPECTED_RESULTS = (
            "<NMEA(PQTMCOLD)>",
            "<NMEA(PQTMWARM)>",
            "<NMEA(PQTMHOT)>",
            "<NMEA(PQTMSRR)>",
            "<NMEA(PQTMUNIQID)>",
            "<NMEA(PQTMSAVEPAR)>",
            "<NMEA(PQTMRESTOREPAR)>",
            "<NMEA(PQTMVERNO)>",
            "<NMEA(PQTMCFGUART, status=W, baudrate=115200)>",
            "<NMEA(PQTMCFGUART, status=W, portid=1, baudrate=115200)>",
            "<NMEA(PQTMCFGUART, status=W, baudrate=115200, databit=8, parity=0, stopbit=1, flowctrl=0)>",
            "<NMEA(PQTMCFGUART, status=W, portid=1, baudrate=115200, databit=8, parity=0, stopbit=1, flowctrl=0)>",
            "<NMEA(PQTMCFGPPS, status=W, ppsindex=1, enable=1, duration=100, ppsmode=1, polarity=1, reserved=0)>",
            "<NMEA(PQTMCFGPPS, status=W, ppsindex=1, enable=0)>",
            "<NMEA(PQTMCFGPROT, status=W, porttype=1, portid=1, inputprot=00000005, outputprot=00000005)>",
            "<NMEA(PQTMCFGNMEADP, status=W, utcdp=3, posdp=8, altdp=3, dopdp=2, spddp=3, cogdp=2)>",
            "<NMEA(PQTMCFGMSGRATE, status=W, msgname=GGA, rate=1)>",
            "<NMEA(PQTMCFGMSGRATE, status=W, msgname=PQTMEPE, rate=1, msgver=2)>",
            "<NMEA(PQTMCFGMSGRATE, status=W, msgname=RTCM3-1005, rate=1)>",
            "<NMEA(PQTMCFGMSGRATE, status=W, msgname=RTCM3-107X, rate=1, msgver=0)>",
            "<NMEA(PQTMCFGMSGRATE, status=W, msgname=RTCM3-1019, rate=1)>",
            "<NMEA(PQTMCFGGEOFENCE, status=W, geofenceindex=0, geofencemode=0)>",
            "<NMEA(PQTMGNSSSTART)>",
            "<NMEA(PQTMGNSSSTOP)>",
            "<NMEA(PQTMCFGSVIN, status=W, svinmode=1, cfgcnt=3600, acclimit=1.2, ecefx=-2519265.0514, ecefy=4849534.9045, ecefz=3277834.6432)>",
            "<NMEA(PQTMCFGRCVRMODE, status=W, rcvrmode=2)>",
            "<NMEA(PQTMDEBUGON)>",
            "<NMEA(PQTMDEBUGOFF)>",
            "<NMEA(PQTMCFGFIXRATE, status=W, fixinterval=1000)>",
            "<NMEA(PQTMCFGRTK, status=W, diffmode=1, relmode=1)>",
            "<NMEA(PQTMCFGCNST, status=W, gps=1, glonass=1, galileo=1, beidou=1, qzss=0, navic=0)>",
            "<NMEA(PQTMCFGODO, status=W, state=1, initdist=10.5)>",
            "<NMEA(PQTMRESETODO)>",
            "<NMEA(PQTMCFGSIGNAL, status=W, gpssig=7, glonasssig=3, galileosig=F, beidousig=3F, qzsssig=7, navicsig=1)>",
            "<NMEA(PQTMCFGSAT, status=W, systemid=1, signalid=1, masklow=FFFFFFFF)>",
            "<NMEA(PQTMCFGSAT, status=W, systemid=4, signalid=1, masklow=BFFCBFFF, maskhigh=1C003FFF)>",
            "<NMEA(PQTMCFGRSID, status=W, rsid=1024)>",
            "<NMEA(PQTMCFGRTCM, status=W, msmtype=4, msmmode=0, msmelevthd=-90, reserved1=07, reserved2=06, ephmode=1, ephinterval=0)>",
        )
        i = 0
        raw = 0
        with open(os.path.join(DIRNAME, "quectel_nmea_command.log"), "rb") as stream:
            nmr = NMEAReader(
                stream, validate=VALCKSUM | VALMSGID, quitonerror=2, msgmode=SET
            )
            for raw, parsed in nmr:
                if raw is not None:
                    # print(f'"{parsed}",')
                    self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                    i += 1
        self.assertEqual(i, len(EXPECTED_RESULTS))

    def testNMEAQUECTELRESPONSE(
        self,
    ):  # test proprietary Quectel LG290P Response (GET) messages
        EXPECTED_RESULTS = (
            "<NMEA(PQTMVER, msgver=1, vername=MODULE, verstr=LG290P03AANR01A03S, builddate=2024/04/30, buildtime=10:53:07)>",
            "<NMEA(PQTMUNIQID, status=OK, length=16, ID=81D62010EE0AF375BDF5952CDC3757A1)>",
            "<NMEA(PQTMSAVEPAR, status=OK)>",
            "<NMEA(PQTMRESTOREPAR, status=OK)>",
            "<NMEA(PQTMVERNO, verstr=LG290P03AANR01A03S, builddate=2024/04/30, buildtime=10:53:07)>",
            "<NMEA(PQTMCFGUART, status=OK)>",
            "<NMEA(PQTMCFGUART, status=OK)>",
            "<NMEA(PQTMCFGUART, status=OK)>",
            "<NMEA(PQTMCFGUART, status=OK)>",
            "<NMEA(PQTMCFGUART, status=OK, portid=1, baudrate=115200, databit=8, parity=0, stopbit=1, flowctrl=0)>",
            "<NMEA(PQTMCFGUART, status=OK, portid=1, baudrate=115200, databit=8, parity=0, stopbit=1, flowctrl=0)>",
            "<NMEA(PQTMCFGPPS, status=OK)>",
            "<NMEA(PQTMCFGPPS, status=OK, ppsindex=1, enable=1, duration=100, ppsmode=1, polarity=1, reserved=0)>",
            "<NMEA(PQTMCFGPPS, status=OK)>",
            "<NMEA(PQTMCFGPROT, status=OK)>",
            "<NMEA(PQTMCFGPROT, status=OK, porttype=1, portid=1, inputprot=00000005, outputprot=00000005)>",
            "<NMEA(PQTMCFGNMEADP, status=OK)>",
            "<NMEA(PQTMCFGNMEADP, status=OK, utcdp=3, posdp=8, altdp=3, dopdp=2, spddp=3, cogdp=2)>",
            "<NMEA(PQTMEPE, msgver=2, epenorth=1.0, epeeast=1.0, epedown=1.0, epe2d=1.414, epe3d=1.732)>",
            "<NMEA(PQTMCFGMSGRATE, status=OK)>",
            "<NMEA(PQTMCFGMSGRATE, status=OK, msgname=GGA, rate=1, msgver=)>",
            "<NMEA(PQTMCFGMSGRATE, status=OK)>",
            "<NMEA(PQTMCFGMSGRATE, status=OK, msgname=PQTMEPE, rate=1, msgver=2)>",
            "<NMEA(PQTMCFGMSGRATE, status=OK)>",
            "<NMEA(PQTMCFGMSGRATE, status=OK, msgname=RTCM3-1005, rate=1)>",
            "<NMEA(PQTMCFGMSGRATE, status=OK)>",
            "<NMEA(PQTMCFGMSGRATE, status=OK, msgname=RTCM3-107X, rate=1, msgver=0)>",
            "<NMEA(PQTMCFGMSGRATE, status=OK)>",
            "<NMEA(PQTMCFGMSGRATE, status=OK, msgname=RTCM3-1019, rate=1)>",
            "<NMEA(PQTMVEL, msgver=1, time=15:45:12.100000, veln=1.251, vele=2.452, veld=1.245, gndspd=2.752, spd=3.021, hdg=180.512, gndspdacc=0.124, spdacc=0.254, hdgacc=0.25)>",
            "<NMEA(PQTMCFGGEOFENCE, status=OK)>",
            "<NMEA(PQTMCFGGEOFENCE, status=OK)>",
            "<NMEA(PQTMCFGGEOFENCE, status=OK, geofenceindex=0, geofencemode=1, reserved=0, shape=0, lat0=31.451248, lon0=117.451245, radiuslat1=100.5)>",
            "<NMEA(PQTMCFGGEOFENCE, status=OK, geofenceindex=0, geofencemode=0)>",
            "<NMEA(PQTMGEOFENCESTATUS, msgver=1, time=12:45:21, staten_01=1, staten_02=2, staten_03=2, staten_04=2)>",
            "<NMEA(PQTMGNSSSTART, status=OK)>",
            "<NMEA(PQTMGNSSSTOP, status=OK)>",
            "<NMEA(PQTMTXT, msgver=1, totalsennum=1, sennum=1, textid=1, text=0x105f0cf810417c00)>",
            "<NMEA(PQTMCFGSVIN, status=OK)>",
            "<NMEA(PQTMCFGSVIN, status=OK, svinmode=1, cfgcnt=3600, acclimit=1.2, ecefx=-2519265.0514, ecefy=4849534.9045, ecefz=3277834.6432)>",
            "<NMEA(PQTMSVINSTATUS, msgver=1, tow=1000, valid=1, reserved0=, reserved1=1, obs=20, cfgdur=100, meanx=-2484434.3645, meany=4875976.9741, meanz=3266161.3412, meanacc=1.2415)>",
            "<NMEA(PQTMPVT, msgver=1, tow=1000, date=20221225, time=16:33:55, reserved=, fixtype=0, numsv=0, leaps=, lat=, lon=, alt=, sep=, veln=, vele=, veld=, spd=, hdg=, hdop=99.99, pdop=99.99)>",
            "<NMEA(PQTMPVT, msgver=1, tow=31075000, date=20221225, time=08:37:37, reserved=, fixtype=3, numsv=9, leaps=18, lat=31.12738291, lon=117.2637291, alt=34.212, sep=5.267, veln=3.212, vele=2.928, veld=0.238, spd=4.346, hdg=34.12, hdop=2.16, pdop=4.38)>",
            "<NMEA(PQTMCFGRCVRMODE, status=OK)>",
            "<NMEA(PQTMCFGRCVRMODE, status=OK, rcvrmode=2)>",
            "<NMEA(PQTMDEBUGON, status=OK)>",
            "<NMEA(PQTMDEBUGOFF, status=OK)>",
            "<NMEA(PQTMCFGFIXRATE, status=OK)>",
            "<NMEA(PQTMCFGFIXRATE, status=OK, fixinterval=1000)>",
            "<NMEA(PQTMCFGRTK, status=OK)>",
            "<NMEA(PQTMCFGRTK, status=OK, diffmode=1, relmode=1)>",
            "<NMEA(PQTMCFGCNST, status=OK)>",
            "<NMEA(PQTMCFGCNST, status=OK, gps=1, glonass=1, galileo=1, beidou=1, qzss=0, navic=0)>",
            "<NMEA(PQTMDOP, msgver=1, tow=570643000, gdop=1.01, pdop=0.88, tdop=0.49, vdop=0.73, hdop=0.5, ndop=0.36, edop=0.35)>",
            "<NMEA(PQTMDOP, msgver=1, tow=, gdop=99.99, pdop=99.99, tdop=99.99, vdop=99.99, hdop=99.99, ndop=99.99, edop=99.99)>",
            "<NMEA(PQTMPL, msgver=1, tow=55045200, pul=5.0, reserved1=1, reserved2=1, plposn=2879.0, plpose=2718.0, plposd=4766.0, plveln=5344.0, plvele=4323.0, plveld=10902.0, reserved3=, reserved4=, pltime=)>",
            "<NMEA(PQTMCFGODO, status=OK)>",
            "<NMEA(PQTMCFGODO, status=ERROR, errcode=1)>",
            "<NMEA(PQTMCFGODO, status=OK, state=1, initdist=10.5)>",
            "<NMEA(PQTMRESETODO, status=OK)>",
            "<NMEA(PQTMODO, msgver=1, time=12:06:35, state=1, dist=112.3)>",
            "<NMEA(PQTMCFGSIGNAL, status=OK)>",
            "<NMEA(PQTMCFGSIGNAL, status=OK, gpssig=07, glonasssig=03, galileosig=0F, beidousig=3F, qzsssig=07, navicsig=01)>",
            "<NMEA(PQTMCFGSAT, status=OK)>",
            "<NMEA(PQTMCFGSAT, status=OK, systemid=1, signalid=01, masklow=FFFFFFFF)>",
            "<NMEA(PQTMCFGSAT, status=OK)>",
            "<NMEA(PQTMCFGSAT, status=ERROR, errcode=2)>",
            "<NMEA(PQTMCFGRSID, status=OK)>",
            "<NMEA(PQTMCFGRSID, status=OK, rsid=1024)>",
            "<NMEA(PQTMCFGRTCM, status=OK)>",
            "<NMEA(PQTMCFGGEOFENCE, status=R, geofenceindex=0, geofencemode=1, reserved=0, shape=3, lat0=31.451248, lon0=117.451245, radiuslat1=100.5, lon1=12.36, lat2=85.24, lon2=118.72, lat3=56.45, lon3=140.13)>",
        )
        i = 0
        raw = 0
        with open(os.path.join(DIRNAME, "quectel_nmea_response.log"), "rb") as stream:
            nmr = NMEAReader(
                stream, validate=VALCKSUM | VALMSGID, quitonerror=1, msgmode=GET
            )
            for raw, parsed in nmr:
                if raw is not None:
                    # print(f'"{parsed}",')
                    self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                    i += 1
        self.assertEqual(i, len(EXPECTED_RESULTS))

    def testConstructors_QUECTEL(self):  # test Quectel constructors
        EXPECTED_PARSED = [
            "<NMEA(PQTMCFGPPS, status=R, ppsindex=0)>",
            "<NMEA(PQTMCFGPPS, status=OK, ppsindex=0, enable=0, duration=0, ppsmode=0, polarity=0, reserved=0)>",
            "<NMEA(PQTMCFGUART, status=W, baudrate=115200)>",
            "<NMEA(PQTMCFGUART, status=W, portid=1, baudrate=115200)>",
            "<NMEA(PQTMCFGUART, status=W, baudrate=115200, databit=8, parity=0, stopbit=1, flowctrl=0)>",
            "<NMEA(PQTMCFGUART, status=W, portid=1, baudrate=115200, databit=8, parity=0, stopbit=0, flowctrl=0)>",
            "<NMEA(PQTMCFGUART, status=R)>",
            "<NMEA(PQTMCFGUART, status=R, portid=1)>",
            "<NMEA(PQTMCFGMSGRATE, status=W, msgname=GLL, rate=1)>",
            "<NMEA(PQTMCFGMSGRATE, status=W, msgname=GLL, rate=1, msgver=2)>",
            "<NMEA(PQTMCFGMSGRATE, status=R, msgname=GLL)>",
            "<NMEA(PQTMCFGMSGRATE, status=R, msgname=PQTMEPE, msgver=2)>",
            "<NMEA(PQTMVERNO)>",
            "<NMEA(PQTMVER, msgver=1, vername=MODULE, verstr=LG290P03AANR01A03S, builddate=2024/04/30, buildtime=10:53:07)>",
            "<NMEA(PQTMHOT)>",
            "<NMEA(PQTMWARM)>",
            "<NMEA(PQTMCOLD)>",
            "<NMEA(PQTMGNSSSTART)>",
            "<NMEA(PQTMGNSSSTOP)>",
            "<NMEA(PQTMDEBUGON)>",
            "<NMEA(PQTMDEBUGOFF)>",
            "<NMEA(PQTMUNIQID)>",
            "<NMEA(PQTMRESETODO)>",
            "<NMEA(PQTMRESTOREPAR)>",
            "<NMEA(PQTMSAVEPAR)>",
            "<NMEA(PQTMCFGCNST, status=W, gps=1, glonass=1, galileo=1, beidou=1, qzss=0, navic=0)>",
            "<NMEA(PQTMCFGFIXRATE, status=W, fixinterval=1000)>",
            "<NMEA(PQTMSRR)>",
            "<NMEA(PQTMCFGRSID, status=W, rsid=1024)>",
            "<NMEA(PQTMCFGPROT, status=W, porttype=1, portid=1, inputprot=00000005, outputprot=00000005)>",
            "<NMEA(PQTMCFGNMEADP, status=W, utcdp=3, posdp=8, altdp=3, dopdp=2, spddp=3, cogdp=2)>",
            "<NMEA(PQTMCFGODO, status=W, state=1, initdist=10.5)>",
            "<NMEA(PQTMCFGPPS, status=W, ppsindex=1, enable=1, duration=100, ppsmode=1, polarity=1, reserved=0)>",
            "<NMEA(PQTMCFGRCVRMODE, status=W, rcvrmode=2)>",
            "<NMEA(PQTMCFGRTCM, status=W, msmtype=4, msmmode=0, msmelevthd=-90, reserved1=07, reserved2=06, ephmode=1, ephinterval=0)>",
            "<NMEA(PQTMCFGRTK, status=W, diffmode=1, relmode=1)>",
            "<NMEA(PQTMCFGSAT, status=W, systemid=1, signalid=1, masklow=FFFFFFFF)>",
            "<NMEA(PQTMCFGSAT, status=W, systemid=4, signalid=1, masklow=BFFCBFFF, maskhigh=1C003FFF)>",
            "<NMEA(PQTMCFGSIGNAL, status=W, gpssig=7, glonasssig=3, galileosig=F, beidousig=3F, qzsssig=7, navicsig=1)>",
            "<NMEA(PQTMCFGSVIN, status=W, svinmode=1, cfgcnt=3600, acclimit=1.2, ecefx=-2519265.0514, ecefy=4849534.9045, ecefz=3277834.6432)>",
            "<NMEA(PQTMCFGGEOFENCE, status=W, geofenceindex=0, geofencemode=1, reserved=0, shape=0, lat0=31.451248, lon0=117.451245, radiuslat1=100.5)>",
            "<NMEA(PQTMCFGGEOFENCE, status=W, geofenceindex=0, geofencemode=1, reserved=0, shape=3, lat0=31.451248, lon0=117.451245, radiuslat1=100.5, lon1=12.36, lat2=85.24, lon2=118.72, lat3=56.45, lon3=140.13)>",
            "<NMEA(PQTMCFGPPS, status=R, ppsindex=1)>",
            "<NMEA(PQTMCFGPPS, status=W, ppsindex=1, enable=0)>",
            "<NMEA(PQTMCFGPROT, status=R, porttype=1, portid=1)>",
            "<NMEA(PQTMCFGNMEADP, status=R)>",
            "<NMEA(PQTMCFGMSGRATE, status=R, msgname=GGA)>",
            "<NMEA(PQTMCFGGEOFENCE, status=W, geofenceindex=0, geofencemode=0)>",
            "<NMEA(PQTMCFGGEOFENCE, status=R, geofenceindex=0)>",
            "<NMEA(PQTMCFGSVIN, status=R)>",
            "<NMEA(PQTMCFGRCVRMODE, status=R)>",
            "<NMEA(PQTMCFGFIXRATE, status=R)>",
            "<NMEA(PQTMCFGRTK, status=R)>",
            "<NMEA(PQTMCFGCNST, status=R)>",
            "<NMEA(PQTMCFGODO, status=R)>",
            "<NMEA(PQTMCFGSIGNAL, status=R)>",
            "<NMEA(PQTMCFGSAT, status=R, systemid=1, signalid=1)>",
            "<NMEA(PQTMCFGRSID, status=R)>",
        ]
        EXPECTED_BINARY = [
            "$PQTMCFGPPS,R,0*6B\r\n",
            "$PQTMCFGPPS,OK,0,0,0,0,0,0*21\r\n",
            "$PQTMCFGUART,W,115200*18\r\n",
            "$PQTMCFGUART,W,1,115200*05\r\n",
            "$PQTMCFGUART,W,115200,8,0,1,0*11\r\n",
            "$PQTMCFGUART,W,1,115200,8,0,0,0*0D\r\n",
            "$PQTMCFGUART,R*36\r\n",
            "$PQTMCFGUART,R,1*2B\r\n",
            "$PQTMCFGMSGRATE,W,GLL,1*0C\r\n",
            "$PQTMCFGMSGRATE,W,GLL,1,2*12\r\n",
            "$PQTMCFGMSGRATE,R,GLL*14\r\n",
            "$PQTMCFGMSGRATE,R,PQTMEPE,2*05\r\n",
            "$PQTMVERNO*58\r\n",
            "$PQTMVER,1,MODULE,LG290P03AANR01A03S,2024/04/30,10:53:07*32\r\n",
            "$PQTMHOT*4B\r\n",
            "$PQTMWARM*11\r\n",
            "$PQTMCOLD*1C\r\n",
            "$PQTMGNSSSTART*51\r\n",
            "$PQTMGNSSSTOP*09\r\n",
            "$PQTMDEBUGON*48\r\n",
            "$PQTMDEBUGOFF*06\r\n",
            "$PQTMUNIQID*16\r\n",
            "$PQTMRESETODO*09\r\n",
            "$PQTMRESTOREPAR*13\r\n",
            "$PQTMSAVEPAR*5A\r\n",
            "$PQTMCFGCNST,W,1,1,1,1,0,0*2B\r\n",
            "$PQTMCFGFIXRATE,W,1000*59\r\n",
            "$PQTMSRR*4B\r\n",
            "$PQTMCFGRSID,W,1024*06\r\n",
            "$PQTMCFGPROT,W,1,1,00000005,00000005*38\r\n",
            "$PQTMCFGNMEADP,W,3,8,3,2,3,2*39\r\n",
            "$PQTMCFGODO,W,1,10.5*4E\r\n",
            "$PQTMCFGPPS,W,1,1,100,1,1,0*73\r\n",
            "$PQTMCFGRCVRMODE,W,2*29\r\n",
            "$PQTMCFGRTCM,W,4,0,-90,07,06,1,0*25\r\n",
            "$PQTMCFGRTK,W,1,1*6C\r\n",
            "$PQTMCFGSAT,W,1,1,FFFFFFFF*4B\r\n",
            "$PQTMCFGSAT,W,4,1,BFFCBFFF,1C003FFF*60\r\n",
            "$PQTMCFGSIGNAL,W,7,3,F,3F,7,1*0E\r\n",
            "$PQTMCFGSVIN,W,1,3600,1.2,-2519265.0514,4849534.9045,3277834.6432*01\r\n",
            "$PQTMCFGGEOFENCE,W,0,1,0,0,31.451248,117.451245,100.5*18\r\n",
            "$PQTMCFGGEOFENCE,W,0,1,0,3,31.451248,117.451245,100.5,12.36,85.24,118.72,56.45,140.13*1C\r\n",
            "$PQTMCFGPPS,R,1*6A\r\n",
            "$PQTMCFGPPS,W,1,0*73\r\n",
            "$PQTMCFGPROT,R,1,1*3D\r\n",
            "$PQTMCFGNMEADP,R*37\r\n",
            "$PQTMCFGMSGRATE,R,GGA*12\r\n",
            "$PQTMCFGGEOFENCE,W,0,0*27\r\n",
            "$PQTMCFGGEOFENCE,R,0*3E\r\n",
            "$PQTMCFGSVIN,R*26\r\n",
            "$PQTMCFGRCVRMODE,R*32\r\n",
            "$PQTMCFGFIXRATE,R*71\r\n",
            "$PQTMCFGRTK,R*69\r\n",
            "$PQTMCFGCNST,R*2E\r\n",
            "$PQTMCFGODO,R*60\r\n",
            "$PQTMCFGSIGNAL,R*3A\r\n",
            "$PQTMCFGSAT,R,1,1*62\r\n",
            "$PQTMCFGRSID,R*28\r\n",
        ]
        msgs = [
            NMEAMessage("P", "QTMCFGPPS", POLL),
            NMEAMessage("P", "QTMCFGPPS", GET),
            NMEAMessage("P", "QTMCFGUART", SET, baudrate=115200),
            NMEAMessage("P", "QTMCFGUART", SET, portid=1, baudrate=115200),
            NMEAMessage("P", "QTMCFGUART", SET, baudrate=115200, databit=8, stopbit=1),
            NMEAMessage("P", "QTMCFGUART", SET, portid=1, baudrate=115200, databit=8),
            NMEAMessage("P", "QTMCFGUART", POLL),
            NMEAMessage("P", "QTMCFGUART", POLL, portid=1),
            NMEAMessage("P", "QTMCFGMSGRATE", SET, msgname="GLL", rate=1),
            NMEAMessage("P", "QTMCFGMSGRATE", SET, msgname="GLL", rate=1, msgver=2),
            NMEAMessage("P", "QTMCFGMSGRATE", POLL, msgname="GLL"),
            NMEAMessage("P", "QTMCFGMSGRATE", POLL, msgname="PQTMEPE", msgver=2),
            NMEAMessage("P", "QTMVERNO", POLL),
            NMEAMessage(
                "P",
                "QTMVER",
                GET,
                msgver=1,
                vername="MODULE",
                verstr="LG290P03AANR01A03S",
                builddate="2024/04/30",
                buildtime="10:53:07",
            ),
            NMEAMessage("P", "QTMHOT", SET),
            NMEAMessage("P", "QTMWARM", SET),
            NMEAMessage("P", "QTMCOLD", SET),
            NMEAMessage("P", "QTMGNSSSTART", SET),
            NMEAMessage("P", "QTMGNSSSTOP", SET),
            NMEAMessage("P", "QTMDEBUGON", SET),
            NMEAMessage("P", "QTMDEBUGOFF", SET),
            NMEAMessage("P", "QTMUNIQID", SET),
            NMEAMessage("P", "QTMRESETODO", SET),
            NMEAMessage("P", "QTMRESTOREPAR", SET),
            NMEAMessage("P", "QTMSAVEPAR", SET),
            NMEAMessage(
                "P",
                "QTMCFGCNST",
                SET,
                gps=1,
                glonass=1,
                galileo=1,
                beidou=1,
                qzss=0,
                navic=0,
            ),
            NMEAMessage("P", "QTMCFGFIXRATE", SET, fixinterval=1000),
            NMEAMessage("P", "QTMSRR", SET),
            NMEAMessage("P", "QTMCFGRSID", SET, rsid=1024),
            NMEAMessage(
                "P",
                "QTMCFGPROT",
                SET,
                porttype=1,
                portid=1,
                inputprot=hex2str(0x05, 8),  # hex as padded string
                outputprot=hex2str(0x05, 8),  # hex as padded string
            ),
            NMEAMessage(
                "P",
                "QTMCFGNMEADP",
                SET,
                utcdp=3,
                posdp=8,
                altdp=3,
                dopdp=2,
                spddp=3,
                cogdp=2,
            ),
            NMEAMessage(
                "P",
                "QTMCFGODO",
                SET,
                state=1,
                initdist=10.5,
            ),
            NMEAMessage(
                "P",
                "QTMCFGPPS",
                SET,
                ppsindex=1,
                enable=1,
                duration=100,
                ppsmode=1,
                polarity=1,
            ),
            NMEAMessage("P", "QTMCFGRCVRMODE", SET, rcvrmode=2),
            NMEAMessage(
                "P",
                "QTMCFGRTCM",
                SET,
                msmtype=4,
                msmmode=0,
                msmelevthd=-90,
                reserved1="07",
                reserved2="06",
                ephmode=1,
                ephinterval=0,
            ),
            NMEAMessage("P", "QTMCFGRTK", SET, diffmode=1, relmode=1),
            NMEAMessage(
                "P",
                "QTMCFGSAT",
                SET,
                systemid=1,
                signalid=1,
                masklow=hex2str(0xFFFFFFFF, 8),  # hex as padded string
            ),
            NMEAMessage(
                "P",
                "QTMCFGSAT",
                SET,
                systemid=4,
                signalid=1,
                masklow=hex2str(0xBFFCBFFF, 8),  # hex as padded string
                maskhigh=hex2str(0x1C003FFF, 8),  # hex as padded string
            ),
            NMEAMessage(
                "P",
                "QTMCFGSIGNAL",
                SET,
                gpssig=hex2str(0x07),  # hex as unpadded string
                glonasssig=hex2str(0x03),
                galileosig=hex2str(0x0F),
                beidousig=hex2str(0x3F),
                qzsssig=hex2str(0x07),
                navicsig=hex2str(0x01),
            ),
            NMEAMessage(
                "P",
                "QTMCFGSVIN",
                SET,
                svinmode=1,
                cfgcnt=3600,
                acclimit=1.2,
                ecefx=-2519265.0514,
                ecefy=4849534.9045,
                ecefz=3277834.6432,
            ),
            NMEAMessage(
                "P",
                "QTMCFGGEOFENCE",
                SET,
                geofenceindex=0,
                geofencemode=1,
                shape=0,
                lat0=31.451248,
                lon0=117.451245,
                radiuslat1=100.5,
            ),
            NMEAMessage(
                "P",
                "QTMCFGGEOFENCE",
                SET,
                geofenceindex=0,
                geofencemode=1,
                shape=3,
                lat0=31.451248,
                lon0=117.451245,
                radiuslat1=100.5,
                lon1=12.36,
                lat2=85.24,
                lon2=118.72,
                lat3=56.45,
                lon3=140.13,
            ),
            NMEAMessage(
                "P",
                "QTMCFGPPS",
                POLL,
                ppsindex=1,
            ),
            NMEAMessage(
                "P",
                "QTMCFGPPS",
                SET,
                ppsindex=1,
                enable=0,
            ),
            NMEAMessage(
                "P",
                "QTMCFGPROT",
                POLL,
                porttype=1,
                portid=1,
            ),
            NMEAMessage(
                "P",
                "QTMCFGNMEADP",
                POLL,
            ),
            NMEAMessage("P", "QTMCFGMSGRATE", POLL, msgname="GGA"),
            NMEAMessage(
                "P",
                "QTMCFGGEOFENCE",
                SET,
                geofenceindex=0,
                geofencemode=0,
            ),
            NMEAMessage(
                "P",
                "QTMCFGGEOFENCE",
                POLL,
                geofenceindex=0,
            ),
            NMEAMessage(
                "P",
                "QTMCFGSVIN",
                POLL,
            ),
            NMEAMessage("P", "QTMCFGRCVRMODE", POLL),
            NMEAMessage("P", "QTMCFGFIXRATE", POLL),
            NMEAMessage("P", "QTMCFGRTK", POLL),
            NMEAMessage("P", "QTMCFGCNST", POLL),
            NMEAMessage("P", "QTMCFGODO", POLL),
            NMEAMessage("P", "QTMCFGSIGNAL", POLL),
            NMEAMessage("P", "QTMCFGSAT", POLL, systemid=1, signalid=1),
            NMEAMessage("P", "QTMCFGRSID", POLL),
        ]
        for i, msg in enumerate(msgs):
            self.assertEqual(str(msg), EXPECTED_PARSED[i])
            self.assertEqual(msg.serialize().decode(), EXPECTED_BINARY[i])
