"""
Stream method tests for pynmeagps

Created on 4 Mar 2021

*** NB: must be saved in UTF-8 format ***

:author: semuadmin (Steve Smith)
"""

import os
import sys
import unittest
from logging import ERROR

from pynmeagps import (
    NMEAReader,
    NMEAParseError,
    NMEATypeError,
    VALCKSUM,
    ERR_RAISE,
    ERR_IGNORE,
    ERR_LOG,
    GET,
    SET,
    TM,
    LA,
    LAD,
    LN,
    LND,
    ST,
    FMI_STATUS,
)

DIRNAME = os.path.dirname(__file__)


class StreamTest(unittest.TestCase):
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

    def testNMEASTARTUP(self):  # stream of NMEA device during start up (blank data)
        EXPECTED_RESULTS = (
            "<NMEA(GNRMC, time=, status=V, lat=, NS=, lon=, EW=, spd=, cog=, date=, mv=, mvEW=, posMode=N, navStatus=V)>",
            "<NMEA(GNVTG, cogt=, cogtUnit=, cogm=, cogmUnit=, sogn=, sognUnit=, sogk=, sogkUnit=, posMode=N)>",
            "<NMEA(GNGGA, time=, lat=, NS=, lon=, EW=, quality=0, numSV=0, HDOP=99.99, alt=, altUnit=, sep=, sepUnit=, diffAge=, diffStation=)>",
            "<NMEA(GNGSA, opMode=A, navMode=1, svid_01=, svid_02=, svid_03=, svid_04=, svid_05=, svid_06=, svid_07=, svid_08=, svid_09=, svid_10=, svid_11=, svid_12=, PDOP=99.99, HDOP=99.99, VDOP=99.99, systemId=1)>",
            "<NMEA(GNGSA, opMode=A, navMode=1, svid_01=, svid_02=, svid_03=, svid_04=, svid_05=, svid_06=, svid_07=, svid_08=, svid_09=, svid_10=, svid_11=, svid_12=, PDOP=99.99, HDOP=99.99, VDOP=99.99, systemId=2)>",
            "<NMEA(GNGSA, opMode=A, navMode=1, svid_01=, svid_02=, svid_03=, svid_04=, svid_05=, svid_06=, svid_07=, svid_08=, svid_09=, svid_10=, svid_11=, svid_12=, PDOP=99.99, HDOP=99.99, VDOP=99.99, systemId=3)>",
            "<NMEA(GNGSA, opMode=A, navMode=1, svid_01=, svid_02=, svid_03=, svid_04=, svid_05=, svid_06=, svid_07=, svid_08=, svid_09=, svid_10=, svid_11=, svid_12=, PDOP=99.99, HDOP=99.99, VDOP=99.99, systemId=4)>",
            "<NMEA(GPGSV, numMsg=1, msgNum=1, numSV=0, signalID=1)>",
            "<NMEA(GLGSV, numMsg=1, msgNum=1, numSV=0, signalID=1)>",
            "<NMEA(GAGSV, numMsg=1, msgNum=1, numSV=0, signalID=7)>",
            "<NMEA(GBGSV, numMsg=1, msgNum=1, numSV=0, signalID=1)>",
            "<NMEA(GNGLL, lat=, NS=, lon=, EW=, time=, status=V, posMode=N)>",
        )

        i = 0
        raw = 0
        with open(os.path.join(DIRNAME, "pygpsdata-nmeastartup.log"), "rb") as stream:
            nmr = NMEAReader(stream, nmeaonly=False, validate=1)
            while raw is not None:
                (raw, parsed) = nmr.read()
                if raw is not None:
                    self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                    i += 1
        self.assertEqual(
            i, 12
        )  # if this fails, may be because log file terminators = LF rather than CRLF

    def testNMEA4(
        self,
    ):  # stream of NMEA v4.10 device (u-blox M9N) (NB everything after PUBX is synthetic)
        EXPECTED_RESULTS = (
            "<NMEA(GNDTM, datum=W84, subDatum=, latOfset=0.0, NS=N, lonOfset=0.0, EW=E, alt=0.0, refDatum=W84)>",
            "<NMEA(GNRMC, time=10:36:07, status=A, lat=53.450657, NS=N, lon=-102.2404103333, EW=W, spd=0.046, cog=, date=2021-03-06, mv=, mvEW=, posMode=A, navStatus=V)>",
            "<NMEA(GPRTE, numMsg=2, msgNum=1, status=c, routeid=0, wpt_01=PBRCPK, wpt_02=PBRTO, wpt_03=PTELGR, wpt_04=PPLAND, wpt_05=PYAMBU, wpt_06=PPFAIR, wpt_07=PWARRN, wpt_08=PMORTL, wpt_09=PLISMR)>",
            "<NMEA(GNRLM, beacon=00000078A9FBAD5, time=08:35:59, code=3, body=C45B)>",
            "<NMEA(GNVTG, cogt=, cogtUnit=T, cogm=, cogmUnit=M, sogn=0.046, sognUnit=N, sogk=0.085, sogkUnit=K, posMode=A)>",
            "<NMEA(GNGNS, time=10:36:07, lat=53.450657, NS=N, lon=-2.2404103333, EW=W, posMode=AANN, numSV=6, HDOP=5.88, alt=56.0, sep=48.5, diffAge=, diffStation=, navStatus=V)>",
            "<NMEA(GNGGA, time=10:36:07, lat=53.450657, NS=N, lon=-2.2404103333, EW=W, quality=1, numSV=6, HDOP=5.88, alt=56.0, altUnit=M, sep=48.5, sepUnit=M, diffAge=, diffStation=)>",
            "<NMEA(GNGSA, opMode=A, navMode=3, svid_01=23, svid_02=24, svid_03=20, svid_04=12, svid_05=, svid_06=, svid_07=, svid_08=, svid_09=, svid_10=, svid_11=, svid_12=, PDOP=9.62, HDOP=5.88, VDOP=7.62, systemId=1)>",
            "<NMEA(GNGSA, opMode=A, navMode=3, svid_01=66, svid_02=76, svid_03=, svid_04=, svid_05=, svid_06=, svid_07=, svid_08=, svid_09=, svid_10=, svid_11=, svid_12=, PDOP=9.62, HDOP=5.88, VDOP=7.62, systemId=2)>",
            "<NMEA(GNGSA, opMode=A, navMode=3, svid_01=, svid_02=, svid_03=, svid_04=, svid_05=, svid_06=, svid_07=, svid_08=, svid_09=, svid_10=, svid_11=, svid_12=, PDOP=9.62, HDOP=5.88, VDOP=7.62, systemId=3)>",
            "<NMEA(GNGSA, opMode=A, navMode=3, svid_01=, svid_02=, svid_03=, svid_04=, svid_05=, svid_06=, svid_07=, svid_08=, svid_09=, svid_10=, svid_11=, svid_12=, PDOP=9.62, HDOP=5.88, VDOP=7.62, systemId=4)>",
            "<NMEA(GPGSV, numMsg=3, msgNum=1, numSV=11, svid_01=1, elv_01=6.0, az_01=14, cno_01=8, svid_02=12, elv_02=43.0, az_02=207, cno_02=28, svid_03=14, elv_03=6.0, az_03=49, cno_03=, svid_04=15, elv_04=44.0, az_04=171, cno_04=23, signalID=1)>",
            "<NMEA(GPGSV, numMsg=3, msgNum=2, numSV=11, svid_01=17, elv_01=32.0, az_01=64, cno_01=16, svid_02=19, elv_02=33.0, az_02=94, cno_02=, svid_03=20, elv_03=20.0, az_03=251, cno_03=31, svid_04=21, elv_04=4.0, az_04=354, cno_04=, signalID=1)>",
            "<NMEA(GPGSV, numMsg=3, msgNum=3, numSV=11, svid_01=23, elv_01=27.0, az_01=251, cno_01=31, svid_02=24, elv_02=89.0, az_02=268, cno_02=26, svid_03=25, elv_03=5.0, az_03=223, cno_03=, signalID=1)>",
            "<NMEA(GLGSV, numMsg=3, msgNum=1, numSV=10, svid_01=65, elv_01=7.0, az_01=176, cno_01=, svid_02=66, elv_02=57.0, az_02=223, cno_02=35, svid_03=67, elv_03=42.0, az_03=315, cno_03=23, svid_04=68, elv_04=0.0, az_04=341, cno_04=29, signalID=1)>",
            "<NMEA(GLGSV, numMsg=3, msgNum=2, numSV=10, svid_01=75, elv_01=37.0, az_01=57, cno_01=, svid_02=76, elv_02=78.0, az_02=303, cno_02=18, svid_03=77, elv_03=27.0, az_03=253, cno_03=21, svid_04=84, elv_04=19.0, az_04=18, cno_04=, signalID=B)>",
            "<NMEA(GLGSV, numMsg=3, msgNum=3, numSV=10, svid_01=85, elv_01=22.0, az_01=78, cno_01=, svid_02=86, elv_02=1.0, az_02=121, cno_02=, signalID=1)>",
            "<NMEA(GAGSV, numMsg=1, msgNum=1, numSV=0, signalID=7)>",
            "<NMEA(GBGSV, numMsg=1, msgNum=1, numSV=2, svid_01=21, elv_01=, az_01=, cno_01=15, svid_02=25, elv_02=, az_02=, cno_02=28, signalID=1)>",
            "<NMEA(GNGLL, lat=53.450657, NS=N, lon=-2.2404103333, EW=W, time=10:36:07, status=A, posMode=A)>",
            "<NMEA(GNGRS, time=10:36:07, mode=1, residual_01=-2.1, residual_02=0.2, residual_03=2.7, residual_04=-0.4, residual_05=, residual_06=, residual_07=, residual_08=, residual_09=, residual_10=, residual_11=, residual_12=, systemId=1, signalId=1)>",
            "<NMEA(GNGRS, time=10:36:07, mode=1, residual_01=0.6, residual_02=5.1, residual_03=, residual_04=, residual_05=, residual_06=, residual_07=, residual_08=, residual_09=, residual_10=, residual_11=, residual_12=, systemId=2, signalId=1)>",
            "<NMEA(GNGRS, time=10:36:07, mode=1, residual_01=, residual_02=, residual_03=, residual_04=, residual_05=, residual_06=, residual_07=, residual_08=, residual_09=, residual_10=, residual_11=, residual_12=, systemId=3, signalId=7)>",
            "<NMEA(GNGRS, time=10:36:07, mode=1, residual_01=, residual_02=, residual_03=, residual_04=, residual_05=, residual_06=, residual_07=, residual_08=, residual_09=, residual_10=, residual_11=, residual_12=, systemId=4, signalId=1)>",
            "<NMEA(GNGST, time=10:36:07, rangeRms=38.0, stdMajor=60.0, stdMinor=38.0, orient=89.0, stdLat=15.0, stdLong=24.0, stdAlt=31.0)>",
            "<NMEA(GNZDA, time=10:36:07, day=6, month=3, year=2021, ltzh=00, ltzn=00)>",
            "<NMEA(GNGBS, time=10:36:07, errLat=15.1, errLon=24.2, errAlt=31.0, svid=, prob=, bias=, stddev=, systemId=, signalId=)>",
            "<NMEA(GNVLW, twd=, twdUnit=N, wd=, wdUnit=N, tgd=0.0, tgdUnit=N, gd=0.0, gdUnit=N)>",
            "<NMEA(PUBX00, msgId=00, time=10:36:07, lat=53.450657, NS=N, lon=-2.2404103333, EW=W, altRef=104.461, navStat=G3, hAcc=29.0, vAcc=31.0, SOG=0.085, COG=39.63, vVel=-0.007, diffAge=, HDOP=5.88, VDOP=7.62, TDOP=8.09, numSVs=6, reserved=0, DR=0)>",
            "<NMEA(PUBX03, msgId=03, numSv=23, svid_01=1, status_01=-, azi_01=14.0, ele_01=6.0, cno_01=8, lck_01=0, svid_02=12, status_02=U, azi_02=207.0, ele_02=43.0, cno_02=28, lck_02=9, svid_03=14, status_03=-, azi_03=49.0, ele_03=6.0, cno_03=, lck_03=0, svid_04=15, status_04=-, azi_04=171.0, ele_04=44.0, cno_04=23, lck_04=0, svid_05=17, status_05=-, azi_05=64.0, ele_05=32.0, cno_05=16, lck_05=0, svid_06=19, status_06=-, azi_06=94.0, ele_06=33.0, cno_06=, lck_06=0, svid_07=20, status_07=U, azi_07=251.0, ele_07=20.0, cno_07=31, lck_07=38, svid_08=21, status_08=-, azi_08=354.0, ele_08=4.0, cno_08=, lck_08=0, svid_09=23, status_09=U, azi_09=251.0, ele_09=27.0, cno_09=31, lck_09=64, svid_10=24, status_10=U, azi_10=268.0, ele_10=89.0, cno_10=26, lck_10=0, svid_11=25, status_11=-, azi_11=223.0, ele_11=5.0, cno_11=, lck_11=0, svid_12=48, status_12=-, azi_12=, ele_12=, cno_12=15, lck_12=0, svid_13=52, status_13=-, azi_13=, ele_13=, cno_13=28, lck_13=13, svid_14=65, status_14=-, azi_14=176.0, ele_14=7.0, cno_14=, lck_14=0, svid_15=66, status_15=U, azi_15=223.0, ele_15=57.0, cno_15=35, lck_15=64, svid_16=67, status_16=-, azi_16=315.0, ele_16=42.0, cno_16=23, lck_16=0, svid_17=68, status_17=-, azi_17=341.0, ele_17=0.0, cno_17=29, lck_17=0, svid_18=75, status_18=-, azi_18=57.0, ele_18=37.0, cno_18=, lck_18=0, svid_19=76, status_19=U, azi_19=303.0, ele_19=78.0, cno_19=18, lck_19=0, svid_20=77, status_20=-, azi_20=253.0, ele_20=27.0, cno_20=21, lck_20=0, svid_21=84, status_21=-, azi_21=18.0, ele_21=19.0, cno_21=, lck_21=0, svid_22=85, status_22=-, azi_22=78.0, ele_22=22.0, cno_22=, lck_22=0, svid_23=86, status_23=-, azi_23=121.0, ele_23=1.0, cno_23=, lck_23=0)>",
            "<NMEA(PUBX04, msgId=04, time=10:36:07, date=2021-03-06, utcTow=556567.00, utcWk=2147, leapSec=18, clkBias=-384839.0, clkDrift=-53.623, tpGran=16)>",
            "<NMEA(GPWPL, lat=49.286, NS=N, lon=-123.1773333333, EW=W, wpt=003)>",
            "<NMEA(GPRMA, status=A, lat=53.450657, NS=N, lon=-112.2404103333, EW=W, reserved1=, reserved2=, sog=23.1, cog=23.0, var=14.8, dirvar=W)>",
            "<NMEA(GPRMB, status=A, ctrkerr=0.66, dirs=L, wptO=003, wptD=004, lat=49.2873333333, NS=N, lon=-123.1595, EW=W, range=1.3, bearing=52.5, velclos=0.5, arrstatus=V)>",
            "<NMEA(PGRME, HPE=15.0, HPEUnit=M, VPE=45.0, VPEUnit=M, EPE=25.0, EPEUnit=M)>",
            "<NMEA(PGRMM, dtm=NAD27 Canada)>",
            "<NMEA(PGRMZ, alt=246.0, altUnit=f, fix=3)>",
            "<NMEA(GPXTE, gwarn=A, LCcwarn=A, ctrkerr=4.07, dirs=L, disUnit=N)>",
            "<NMEA(GPVBW, longwaterspd=12.3, transwaterspd=0.07, waterspdstatus=A, longgroundspd=11.78, transgroundspd=0.12, groundspdstatus=A)>",
            "<NMEA(GPSTN, talkerId=34)>",
            "<NMEA(GPBWC, fixutc=22:05:16, lat=51.5003333333, NS=N, lon=-0.7723333333, EW=W, bearT=213.8, bearTu=T, bearM=218.0, bearMu=M, dist=4.6, distUnit=N, wpt=EGLM)>",
            "<NMEA(GPBOD, bearT=97.0, bearTu=T, bearM=103.2, bearMu=M, wptD=POINTB, wptO=POINTA)>",
            "<NMEA(GPBOD, bearT=99.3, bearTu=T, bearM=105.6, bearMu=M, wptD=POINTB, wptO=)>",
            "<NMEA(GPAAM, arrce=A, perp=A, crad=0.1, cUnit=N, wpt=WPTNME)>",
            "<NMEA(GPAPB, LCgwarn=A, LCcwarn=A, ctrkerr=0.1, dirs=R, ctrkUnit=N, aalmcirc=V, aalmperp=V, bearO2D=11.0, bearO2Du=M, wpt=DEST, bearD=11.0, bearDu=M, bearS=11.0, bearSu=M)>",
            "<NMEA(GPMSK, freq=318.0, fmode=A, beacbps=100, bpsmode=M, MMSfreq=2.0)>",
            "<NMEA(GPMSS, strength=55, snr=27, freq=318.0, beacbps=100, channel=)>",
            "<NMEA(GBGSV, numMsg=2, msgNum=2, numSV=6, svid_01=14, elv_01=55.0, az_01=175, cno_01=46, svid_02=40, elv_02=29.0, az_02=43, cno_02=18, signalID=B)>",
            "<NMEA(INGGA, time=10:36:07, lat=53.450657, NS=N, lon=-2.2404103333, EW=W, quality=1, numSV=6, HDOP=5.88, alt=56.0, altUnit=M, sep=48.5, sepUnit=M, diffAge=, diffStation=)>",
            "<NMEA(ANNAK, talkerid=UP, formatter=AID, identifier=999999990, reason=11, text=)>",
            "<NMEA(GPGBS, time=23:55:03, errLat=1.6, errLon=1.4, errAlt=3.2, svid=, prob=, bias=, stddev=, systemId=, signalId=)>",
            "<NMEA(GPGBS, time=23:54:58, errLat=1.4, errLon=1.3, errAlt=3.1, svid=3, prob=, bias=-21.4, stddev=3.8, systemId=1, signalId=0)>",
        )

        i = 0
        raw = 0
        with open(os.path.join(DIRNAME, "pygpsdata-nmea4.log"), "rb") as stream:
            nmr = NMEAReader(stream, nmeaonly=False, validate=3)
            while raw is not None:
                (raw, parsed) = nmr.read()
                if raw is not None:
                    # print(f'"{parsed}",')
                    self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                    i += 1
        self.assertEqual(i, len(EXPECTED_RESULTS))

    def testNMEA2(self):  # stream of NMEA v2.30 device (u-blox M6N)
        EXPECTED_RESULTS = (
            "<NMEA(GPTXT, numMsg=1, msgNum=1, msgType=2, text=u-blox ag - www.u-blox.com)>",
            "<NMEA(GPTXT, numMsg=1, msgNum=1, msgType=2, text=HW  UBX-G70xx   00070000 )>",
            "<NMEA(GPTXT, numMsg=1, msgNum=1, msgType=2, text=ROM CORE 1.00 (59842) Jun 27 2012 17:43:52)>",
            "<NMEA(GPTXT, numMsg=1, msgNum=1, msgType=2, text=PROTVER 14.00)>",
            "<NMEA(GPTXT, numMsg=1, msgNum=1, msgType=2, text=ANTSUPERV=AC SD PDoS SR)>",
            "<NMEA(GPTXT, numMsg=1, msgNum=1, msgType=2, text=ANTSTATUS=OK)>",
            "<NMEA(GPTXT, numMsg=1, msgNum=1, msgType=2, text=LLC FFFFFFFF-FFFFFFFD-FFFFFFFF-FFFFFFFF-FFFFFFF9)>",
            "<NMEA(GPRMC, time=10:29:29, status=A, lat=53.4506706667, NS=N, lon=-2.24026, EW=W, spd=0.273, cog=, date=2021-03-07, mv=, mvEW=, posMode=A)>",
            "<NMEA(GPVTG, cogt=, cogtUnit=T, cogm=, cogmUnit=M, sogn=0.273, sognUnit=N, sogk=0.506, sogkUnit=K, posMode=A)>",
            "<NMEA(GPGGA, time=10:29:29, lat=53.4506706667, NS=N, lon=-2.24026, EW=W, quality=1, numSV=8, HDOP=1.16, alt=36.3, altUnit=M, sep=48.5, sepUnit=M, diffAge=, diffStation=)>",
            "<NMEA(GPGSA, opMode=A, navMode=3, svid_01=17, svid_02=15, svid_03=10, svid_04=24, svid_05=20, svid_06=12, svid_07=19, svid_08=23, svid_09=, svid_10=, svid_11=, svid_12=, PDOP=2.36, HDOP=1.16, VDOP=2.05)>",
            "<NMEA(GPGSV, numMsg=4, msgNum=1, numSV=15, svid_01=1, elv_01=6.0, az_01=15, cno_01=, svid_02=10, elv_02=30.0, az_02=290, cno_02=27, svid_03=12, elv_03=42.0, az_03=207, cno_03=26, svid_04=13, elv_04=19.0, az_04=141, cno_04=23)>",
            "<NMEA(GPGSV, numMsg=4, msgNum=2, numSV=15, svid_01=14, elv_01=7.0, az_01=49, cno_01=21, svid_02=15, elv_02=45.0, az_02=171, cno_02=27, svid_03=17, elv_03=32.0, az_03=65, cno_03=22, svid_04=19, elv_04=33.0, az_04=95, cno_04=25)>",
            "<NMEA(GPGSV, numMsg=4, msgNum=3, numSV=15, svid_01=20, elv_01=21.0, az_01=251, cno_01=31, svid_02=21, elv_02=4.0, az_02=355, cno_02=, svid_03=23, elv_03=28.0, az_03=252, cno_03=33, svid_04=24, elv_04=88.0, az_04=273, cno_04=36)>",
            "<NMEA(GPGSV, numMsg=4, msgNum=4, numSV=15, svid_01=25, elv_01=5.0, az_01=223, cno_01=, svid_02=28, elv_02=14.0, az_02=49, cno_02=26, svid_03=32, elv_03=10.0, az_03=313, cno_03=16)>",
            "<NMEA(GPGLL, lat=53.4506706667, NS=N, lon=-2.24026, EW=W, time=10:29:29, status=A, posMode=A)>",
            "<NMEA(GPRMC, time=10:29:30, status=A, lat=53.4506721667, NS=N, lon=-2.2402583333, EW=W, spd=0.099, cog=, date=2021-03-07, mv=, mvEW=, posMode=A)>",
        )

        i = 0
        raw = 0
        with open(os.path.join(DIRNAME, "pygpsdata-nmea2.log"), "rb") as stream:
            nmr = NMEAReader(stream, nmeaonly=False)
            while raw is not None:
                (raw, parsed) = nmr.read()
                if raw is not None:
                    self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                    i += 1
        self.assertEqual(i, 17)

    def testMIXED(
        self,
    ):  # stream of mixed NMEA & UBX data with nmea_only set to FALSE - should be ignored
        EXPECTED_RESULTS = (
            "<NMEA(GNGGA, time=10:41:13, lat=53.4505928333, NS=N, lon=-2.2403723333, EW=W, quality=1, numSV=5, HDOP=8.68, alt=65.4, altUnit=M, sep=48.5, sepUnit=M, diffAge=, diffStation=)>",
            "<NMEA(GNGSA, opMode=A, navMode=3, svid_01=20, svid_02=10, svid_03=23, svid_04=, svid_05=, svid_06=, svid_07=, svid_08=, svid_09=, svid_10=, svid_11=, svid_12=, PDOP=12.55, HDOP=8.68, VDOP=9.07, systemId=1)>",
            "<NMEA(GNGSA, opMode=A, navMode=3, svid_01=78, svid_02=68, svid_03=, svid_04=, svid_05=, svid_06=, svid_07=, svid_08=, svid_09=, svid_10=, svid_11=, svid_12=, PDOP=12.55, HDOP=8.68, VDOP=9.07, systemId=2)>",
            "<NMEA(GNGSA, opMode=A, navMode=3, svid_01=, svid_02=, svid_03=, svid_04=, svid_05=, svid_06=, svid_07=, svid_08=, svid_09=, svid_10=, svid_11=, svid_12=, PDOP=12.55, HDOP=8.68, VDOP=9.07, systemId=3)>",
            "<NMEA(GNGSA, opMode=A, navMode=3, svid_01=, svid_02=, svid_03=, svid_04=, svid_05=, svid_06=, svid_07=, svid_08=, svid_09=, svid_10=, svid_11=, svid_12=, PDOP=12.55, HDOP=8.68, VDOP=9.07, systemId=4)>",
            "<NMEA(GPGSV, numMsg=1, msgNum=1, numSV=4, svid_01=10, elv_01=29.0, az_01=284, cno_01=30, svid_02=20, elv_02=17.0, az_02=247, cno_02=36, svid_03=23, elv_03=24.0, az_03=247, cno_03=38, svid_04=28, elv_04=10.0, az_04=49, cno_04=7, signalID=1)>",
            "<NMEA(GLGSV, numMsg=2, msgNum=1, numSV=7, svid_01=66, elv_01=10.0, az_01=179, cno_01=, svid_02=67, elv_02=52.0, az_02=218, cno_02=22, svid_03=68, elv_03=46.0, az_03=309, cno_03=30, svid_04=69, elv_04=5.0, az_04=340, cno_04=17, signalID=1)>",
            "<NMEA(GLGSV, numMsg=2, msgNum=2, numSV=7, svid_01=78, elv_01=30.0, az_01=255, cno_01=33, svid_02=85, elv_02=19.0, az_02=18, cno_02=, svid_03=86, elv_03=25.0, az_03=71, cno_03=, signalID=1)>",
            "<NMEA(GAGSV, numMsg=1, msgNum=1, numSV=0, signalID=7)>",
            "<NMEA(GBGSV, numMsg=1, msgNum=1, numSV=0, signalID=1)>",
            "<NMEA(GNGGA, time=10:41:14, lat=53.4505926667, NS=N, lon=-2.240361, EW=W, quality=1, numSV=5, HDOP=8.68, alt=65.2, altUnit=M, sep=48.5, sepUnit=M, diffAge=, diffStation=)>",
            "<NMEA(GNGSA, opMode=A, navMode=3, svid_01=20, svid_02=10, svid_03=23, svid_04=, svid_05=, svid_06=, svid_07=, svid_08=, svid_09=, svid_10=, svid_11=, svid_12=, PDOP=12.55, HDOP=8.68, VDOP=9.06, systemId=1)>",
            "<NMEA(GNGSA, opMode=A, navMode=3, svid_01=78, svid_02=68, svid_03=, svid_04=, svid_05=, svid_06=, svid_07=, svid_08=, svid_09=, svid_10=, svid_11=, svid_12=, PDOP=12.55, HDOP=8.68, VDOP=9.06, systemId=2)>",
            "<NMEA(GNGSA, opMode=A, navMode=3, svid_01=, svid_02=, svid_03=, svid_04=, svid_05=, svid_06=, svid_07=, svid_08=, svid_09=, svid_10=, svid_11=, svid_12=, PDOP=12.55, HDOP=8.68, VDOP=9.06, systemId=3)>",
            "<NMEA(GNGSA, opMode=A, navMode=3, svid_01=, svid_02=, svid_03=, svid_04=, svid_05=, svid_06=, svid_07=, svid_08=, svid_09=, svid_10=, svid_11=, svid_12=, PDOP=12.55, HDOP=8.68, VDOP=9.06, systemId=4)>",
        )

        i = 0
        raw = 0
        with open(os.path.join(DIRNAME, "pygpsdata-mixed.log"), "rb") as stream:
            nmr = NMEAReader(stream, nmeaonly=False)
            while raw is not None:
                (raw, parsed) = nmr.read()
                if raw is not None:
                    self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                    i += 1
        self.assertEqual(i, 15)

    def testMIXED2(
        self,
    ):  # stream of mixed NMEA & UBX data with nmea_only set to TRUE - should be rejected
        EXPECTED_ERROR = "Unknown protocol header b'$\\x11'"
        with open(os.path.join(DIRNAME, "pygpsdata-mixed.log"), "rb") as stream:
            with self.assertRaises(NMEAParseError) as context:
                i = 0
                raw = 0
                nmr = NMEAReader(stream, nmeaonly=True, quitonerror=ERR_RAISE)
                while raw is not None:
                    (raw, _) = nmr.read()
                    if raw is not None:
                        i += 1
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testNMEAMARITIME(self):  # test NMEA maritime messages
        EXPECTED_RESULTS = (
            "<NMEA(IIALF, numSen=1, senNum=1, seqmid=0, timelastchange=12:43:04.500000, alertcat=A, alertpriority=W, alertstate=A, mfrcode=, alertid=192, alertinst=1, revisionctr=1, escalationctr=0, alerttxt=LOST TARGET)>",
            "<NMEA(IIALF, numSen=2, senNum=1, seqmid=1, timelastchange=08:19:50.100000, alertcat=B, alertpriority=A, alertstate=S, mfrcode=XYZ, alertid=0512, alertinst=1, revisionctr=2, escalationctr=0, alerttxt=HEADING LOST)>",
            "<NMEA(IIALF, numSen=2, senNum=2, seqmid=1, timelastchange=, alertcat=, alertpriority=, alertstate=, mfrcode=XYZ, alertid=0512, alertinst=1, revisionctr=2, escalationctr=0, alerttxt=NO SYSTEM HEADING AVAILABLE)>",
            "<NMEA(AIEPV, status=R, equipmenttype=AI, equipmentid=503123450, propertyid=101, value=38400)>",
            "<NMEA(VRGEN, index=0000, time=01:12:00, data_01=0123, data_02=4567, data_03=89AB, data_04=CDEF, data_05=0123, data_06=4567, data_07=89AB, data_08=CDEF)>",
            "<NMEA(VRGEN, index=0008, time=01:12:00, data_01=0123, data_02=4567)>",
            "<NMEA(INNRM, function=2, freqtable=1, txcovermask=00001E1F, msgtypemask=00000023, status=C)>",
            "<NMEA(CRNRX, numSen=7, senNum=1, seqid=0, msgcode=IE69, freqtable=1, time=13:56:00, day=27, month=6, year=2001, totalchar=241.0, totalbad=3.0, status=A, body=============================)>",
            "<NMEA(CRNRX, numSen=7, senNum=2, seqid=0, msgcode=, freqtable=, time=, day=, month=, year=, totalchar=, totalbad=, status=, body=========^0D^0AISSUED ON SATURDAY 06 JANUARY 2001.)>",
            "<NMEA(CSSM3, MSIstatus=123456, msgnum=5213, LESseqnum=798, LESid=0, oceanregioncode=3, prioritycode=14, servicecode=0, presentationcode=2012, year=4, month=5, day=14, hour=30, minute=3400, circarealat=, circareaNS=076, circarealon=, circareaEW=300)>",
            "<NMEA(CSSMB, numSen=8, senNum=1, seqid=0, msgnum=123456, body=FROM:Maritime Rescue Coordination Centre xxx^0D)0ATO:)>",
            "<NMEA(IISPW, pwdprotectsentence=EPV, id=211000001, pwdlevel=2, password=SESAME)>",
            "<NMEA(IIEPV, status=C, equipmenttype=AI, equipmentid=211000001, propertyid=111, value=HEUREKA143)>",
            "<NMEA(AIEPV, status=R, equipmenttype=AI, equipmentid=211000001, propertyid=111, value=HEUREKA143)>",
        )

        i = 0
        raw = 0
        with open(os.path.join(DIRNAME, "pygpsdata-maritime.log"), "rb") as stream:
            nmr = NMEAReader(stream, nmeaonly=True, quitonerror=2)
            for raw, parsed in nmr:
                if raw is not None:
                    # print(f'"{parsed}",')
                    self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                    i += 1
        self.assertEqual(i, 14)

    def testNMEAITER(self):  # NMEAReader iterator
        EXPECTED_RESULTS = (
            "<NMEA(GNDTM, datum=W84, subDatum=, latOfset=0.0, NS=N, lonOfset=0.0, EW=E, alt=0.0, refDatum=W84)>",
            "<NMEA(GNRMC, time=10:36:07, status=A, lat=53.450657, NS=N, lon=-2.2404103333, EW=W, spd=0.046, cog=, date=2021-03-06, mv=, mvEW=, posMode=A, navStatus=V)>",
            "<NMEA(GNVTG, cogt=, cogtUnit=T, cogm=, cogmUnit=M, sogn=0.046, sognUnit=N, sogk=0.085, sogkUnit=K, posMode=A)>",
            "<NMEA(GNGNS, time=10:36:07, lat=53.450657, NS=N, lon=-2.2404103333, EW=W, posMode=AANN, numSV=6, HDOP=5.88, alt=56.0, sep=48.5, diffAge=, diffStation=, navStatus=V)>",
            "<NMEA(GNGGA, time=10:36:07, lat=53.450657, NS=N, lon=-2.2404103333, EW=W, quality=1, numSV=6, HDOP=5.88, alt=56.0, altUnit=M, sep=48.5, sepUnit=M, diffAge=, diffStation=)>",
            "<NMEA(GNGSA, opMode=A, navMode=3, svid_01=23, svid_02=24, svid_03=20, svid_04=12, svid_05=, svid_06=, svid_07=, svid_08=, svid_09=, svid_10=, svid_11=, svid_12=, PDOP=9.62, HDOP=5.88, VDOP=7.62, systemId=1)>",
            "<NMEA(GPGSV, numMsg=3, msgNum=1, numSV=11, svid_01=1, elv_01=6.0, az_01=14, cno_01=8, svid_02=12, elv_02=43.0, az_02=207, cno_02=28, svid_03=14, elv_03=6.0, az_03=49, cno_03=, svid_04=15, elv_04=44.0, az_04=171, cno_04=23, signalID=1)>",
            "<NMEA(GPTHS, headt=23.34, mi=A)>",
        )

        i = 0
        raw = 0
        with open(os.path.join(DIRNAME, "pygpsdata-nmea4sm.log"), "rb") as stream:
            nmr = NMEAReader(stream, nmeaonly=False)
            for raw, parsed in nmr:
                if raw is not None:
                    self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                    i += 1
        self.assertEqual(i, 8)

    def testNMEAITERATE(self):  # NMEAReader helper method
        EXPECTED_RESULTS = (
            "<NMEA(GNDTM, datum=W84, subDatum=, latOfset=0.0, NS=N, lonOfset=0.0, EW=E, alt=0.0, refDatum=W84)>",
            "<NMEA(GNRMC, time=10:36:07, status=A, lat=53.450657, NS=N, lon=-2.2404103333, EW=W, spd=0.046, cog=, date=2021-03-06, mv=, mvEW=, posMode=A, navStatus=V)>",
            "<NMEA(GNVTG, cogt=, cogtUnit=T, cogm=, cogmUnit=M, sogn=0.046, sognUnit=N, sogk=0.085, sogkUnit=K, posMode=A)>",
            "<NMEA(GNGNS, time=10:36:07, lat=53.450657, NS=N, lon=-2.2404103333, EW=W, posMode=AANN, numSV=6, HDOP=5.88, alt=56.0, sep=48.5, diffAge=, diffStation=, navStatus=V)>",
            "<NMEA(GNGGA, time=10:36:07, lat=53.450657, NS=N, lon=-2.2404103333, EW=W, quality=1, numSV=6, HDOP=5.88, alt=56.0, altUnit=M, sep=48.5, sepUnit=M, diffAge=, diffStation=)>",
            "<NMEA(GNGSA, opMode=A, navMode=3, svid_01=23, svid_02=24, svid_03=20, svid_04=12, svid_05=, svid_06=, svid_07=, svid_08=, svid_09=, svid_10=, svid_11=, svid_12=, PDOP=9.62, HDOP=5.88, VDOP=7.62, systemId=1)>",
            "<NMEA(GPGSV, numMsg=3, msgNum=1, numSV=11, svid_01=1, elv_01=6.0, az_01=14, cno_01=8, svid_02=12, elv_02=43.0, az_02=207, cno_02=28, svid_03=14, elv_03=6.0, az_03=49, cno_03=, svid_04=15, elv_04=44.0, az_04=171, cno_04=23, signalID=1)>",
            "<NMEA(GPTHS, headt=23.34, mi=A)>",
        )

        i = 0
        raw = 0
        with open(os.path.join(DIRNAME, "pygpsdata-nmea4sm.log"), "rb") as stream:
            nmr = NMEAReader(stream, nmeaonly=False)
            for raw, parsed in nmr:
                if raw is not None:
                    self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                    i += 1
        self.assertEqual(i, 8)

    def testNMEAITERATE_ERR1(
        self,
    ):  # NMEAReader iterator with bad checksum
        EXPECTED_ERROR = "Message GNVTG invalid checksum 3) - should be 30"
        with open(os.path.join(DIRNAME, "pygpsdata-nmeabadck2.log"), "rb") as stream:
            with self.assertRaises(NMEAParseError) as context:
                nmr = NMEAReader(
                    stream,
                    nmeaonly=False,
                    validate=VALCKSUM,
                    msgmode=0,
                    quitonerror=ERR_RAISE,
                )
                for raw, parsed in nmr:
                    pass
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testNMEAITERATE_ERR2(
        self,
    ):  # NMEAReader iterator ignoring bad checksum and passing error handler
        EXPECTED_RESULT = "<NMEA(GPGSV, numMsg=3, msgNum=1, numSV=11, svid_01=1, elv_01=0.0, az_01=32, cno_01=, svid_02=10, elv_02=27.0, az_02=310, cno_02=, svid_03=12, elv_03=19.0, az_03=205, cno_03=19, svid_04=13, elv_04=38.0, az_04=134, cno_04=21, signalID=1)>"
        with open(os.path.join(DIRNAME, "pygpsdata-nmeabadck2.log"), "rb") as stream:
            nmr = NMEAReader(
                stream,
                nmeaonly=False,
                validate=VALCKSUM,
                msgmode=0,
                quitonerror=ERR_LOG,
                errorhandler=lambda e: print(f"I ignored the following error: {e}"),
            )
            res = ""
            for raw, parsed in nmr:
                res = str(parsed)
            self.assertEqual(EXPECTED_RESULT, res)

    def testNMEAITERATE_ERR3(
        self,
    ):  # NMEAReader iterator ignoring bad checksum and continuing
        EXPECTED_RESULT = "<NMEA(GPGSV, numMsg=3, msgNum=1, numSV=11, svid_01=1, elv_01=0.0, az_01=32, cno_01=, svid_02=10, elv_02=27.0, az_02=310, cno_02=, svid_03=12, elv_03=19.0, az_03=205, cno_03=19, svid_04=13, elv_04=38.0, az_04=134, cno_04=21, signalID=1)>"
        with open(os.path.join(DIRNAME, "pygpsdata-nmeabadck2.log"), "rb") as stream:
            nmr = NMEAReader(
                stream,
                nmeaonly=False,
                validate=VALCKSUM,
                msgmode=0,
                quitonerror=ERR_IGNORE,
            )
            res = ""
            for raw, parsed in nmr:
                res = str(parsed)
            self.assertEqual(EXPECTED_RESULT, res)

    def testNMEAFOO1(self):  # stream containing invalid attribute type
        EXPECTED_ERROR = "Unknown attribute type Z2"
        with open(os.path.join(DIRNAME, "pygpsdata-nmeafoo1.log"), "rb") as stream:
            with self.assertRaises(NMEATypeError) as context:
                i = 0
                raw = 0
                nmr = NMEAReader(
                    stream,
                    nmeaonly=False,
                    quitonerror=ERR_RAISE,
                )
                for raw, parsed in nmr:
                    i += 1
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testNMEAFOO2(self):  # stream containing invalid value for attribute type
        EXPECTED_ERROR = "Incorrect type for attribute spd in msgID RMC"
        with open(os.path.join(DIRNAME, "pygpsdata-nmeafoo2.log"), "rb") as stream:
            with self.assertRaises(NMEATypeError) as context:
                i = 0
                raw = 0
                nmr = NMEAReader(stream, nmeaonly=False, quitonerror=ERR_RAISE)
                for raw, parsed in nmr:
                    i += 1
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testNMEABADMODE(self):  # invalid stream mode
        EXPECTED_ERROR = "Invalid stream mode 4 - must be 0, 1 or 2."
        with open(os.path.join(DIRNAME, "pygpsdata-nmeafoo1.log"), "rb") as stream:
            with self.assertRaises(NMEAParseError) as context:
                NMEAReader(stream, nmeaonly=False, validate=1, msgmode=4)
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testBADEOF(self):  # stream with premature EOF - should just be tolerated
        EXPECTED_RESULTS = (
            "<NMEA(GNDTM, datum=W84, subDatum=, latOfset=0.0, NS=N, lonOfset=0.0, EW=E, alt=0.0, refDatum=W84)>",
            "<NMEA(GNRMC, time=10:36:07, status=A, lat=53.450657, NS=N, lon=-2.2404103333, EW=W, spd=0.046, cog=, date=2021-03-06, mv=, mvEW=, posMode=A, navStatus=V)>",
            "<NMEA(GNVTG, cogt=, cogtUnit=T, cogm=, cogmUnit=M, sogn=0.046, sognUnit=N, sogk=0.085, sogkUnit=K, posMode=A)>",
            "<NMEA(GNGNS, time=10:36:07, lat=53.450657, NS=N, lon=-2.2404103333, EW=W, posMode=AANN, numSV=6, HDOP=5.88, alt=56.0, sep=48.5, diffAge=, diffStation=, navStatus=V)>",
        )

        i = 0
        raw = 0
        with open(os.path.join(DIRNAME, "pygpsdata-badeof.log"), "rb") as stream:
            nmr = NMEAReader(stream, nmeaonly=False)
            for raw, parsed in nmr:
                if raw is not None:
                    # print(parsed)
                    self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                    i += 1

    def testNMEATRIMBLE(self):  # test proprietary Trimble messages
        EXPECTED_RESULTS = (
            "<NMEA(GPLLQ, utctime=03:41:37, utcdate=2012-07-21, easting=23.45, eunit=M, northing=13.07, nunit=M, gpsQual=3, sip=15, posQual=0.011, height=3.14, hunit=M)>",
            "<NMEA(GPROT, rot=35.6, valid=A)>",
            "<NMEA(PFUGDP, type=GN, utctime=03:36:15, lat=39.8980003333, NS=N, lon=-105.112554, EW=W, siv=13, dpvoaQual=9, dgnssMode=FF, smajErr=0.1, sminErr=0.1, dirErr=149)>",
            "<NMEA(PTNLAVR, msgId=AVR, utctime=21:24:05.200000, yaw=52.1531, yawc=Yaw, tilt=-0.0806, tiltc=Tilt, roll=, rollc=, range=12.575, gpsQual=3, PDOP=1.4, sip=16)>",
            "<NMEA(PTNLAVR, msgId=AVR, utctime=21:26:04.300000, yaw=52.18, yawc=Yaw, tilt=, tiltc=, roll=-0.0807, rollc=Roll, range=12.579, gpsQual=3, PDOP=1.4, sip=16)>",
            "<NMEA(PTNLBPQ, msgId=BPQ, utctime=22:44:45.060000, utcdate=2007-12-02, lat=37.384897319, NS=N, lon=-122.0054366887, EW=W, height=EHT-5.923, hunit=M, gpsQual=5)>",
            "<NMEA(PTNLDG, msgId=DG, strength=44.0, snr=33.0, freq=287.0, bitRate=100, chan=0, trkStatus=4, trkPerf=1)>",
            "<NMEA(PTNLDG, msgId=DG, strength=124.0, snr=10.5, freq=1557855.0, bitRate=1200, chan=2, trkStatus=4, trkPerf=0)>",
            "<NMEA(PTNLEVT, msgId=EVT, utctime=22:12:12.000008, port=1, numEvents=5026, wno=1893, dow=1, leaps=17)>",
            "<NMEA(PTNLEVT, msgId=EVT, utctime=22:12:13.000008, port=1, numEvents=5027, wno=1893, dow=1, leaps=17)>",
            "<NMEA(PTNLGGK, msgId=GGK, utctime=10:29:39, utcdate=, lat=50.0162206402, NS=N, lon=8.4603351237, EW=E, gpsQual=5, sip=9, DOP=1.9, height=EHT150.790, hunit=M)>",
            "<NMEA(PTNLPJK, msgId=PJK, utctime=20:28:31.500000, utcdate=2012-11-01, northing=805083.35, nunit=N, easting=388997.346, eunit=E, gpsQual=10, sip=9, DOP=1.5, height=GHT+25.478, hunit=M)>",
            "<NMEA(PTNLPJK, msgId=PJK, utctime=01:07:17, utcdate=, northing=732646.511, nunit=N, easting=1731051.091, eunit=E, gpsQual=1, sip=5, DOP=2.7, height=EHT+28.345, hunit=M)>",
            "<NMEA(PTNLPJT, msgId=PJT, coordName=NAD83(Conus), projName=California Zone 4 0404)>",
            "<NMEA(PTNLVHD, msgId=VHD, utctime=03:05:56, utcdate=1998-09-30, azi=187.718, aziRate=-22.138, ele=-76.929, eleRate=-5.015, range=0.033, rangeRate=0.006, gpsQual=3, sip=7, PDOP=2.4, unit=M)>",
            "<NMEA(PTNLVGK, msgId=VGK, utctime=16:01:59, utcdate=1997-01-09, vectE=-0.161, vectN=9.985, vectV=-0.002, gpsQual=3, sip=7, DOP=1.0, vunit=4)>",
            "<NMEA(PASHRARR, msgId=ARR, vectNum=1, vectMode=3, sip=12, utctime=16:01:59, antEcefX=123.45, antEcefY=123.45, antEcefZ=-123.45, coord1std=12.34, coord2std=12.34, coord3std=12.34, coord12corr=2.34, coord13corr=2.34, coord23corr=-2.34, refId=S, vectFrame=0, vectOpt=2, clkAssum=1)>",
            "<NMEA(PASHRBTS, msgId=BTS, port_01=C, connected_01=1, name_01=btsdev1, addr_01=hs-344-fg, linkQual_01=87, port_02=H, connected_02=1, name_02=btsdev2, addr_02=pc-377xs, linkQual_02=68, port_03=T, connected_03=0, name_03=, addr_03=, linkQual_03=)>",
            "<NMEA(PGPPADV110, msgId=110, lat=39.88113582, lon=-105.07838455, height=1614.125)>",
            "<NMEA(PGPPADV120, msgId=120, prn_01=21, ele_01=76.82, azi_01=68.51, prn_02=29, ele_02=20.66, azi_02=317.47)>",
            "<NMEA(PASHR, utctime=14:25:09, trueHdg=179.885, trueHdgInd=T, roll=-0.624, pitch=0.245, reserved=, rollAcc=0.029, pitchAcc=0.029, hdgAcc=0.502, gnssQual=2, imuAlign=3)>",
        )

        i = 0
        raw = 0
        with open(os.path.join(DIRNAME, "trimble_nmea.log"), "rb") as stream:
            nmr = NMEAReader(stream, nmeaonly=False)
            for raw, parsed in nmr:
                if raw is not None:
                    # print(parsed)
                    self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                    i += 1
        self.assertEqual(i, 21)

    def testNMEAFURUNO(self):  # test proprietary Furuno messages
        EXPECTED_RESULTS = (
            "<NMEA(PFECGPatt, msgId=GPatt, yaw=12.345, pitch=23.456, roll=34.567)>",
            "<NMEA(PFECGPhve, msgId=GPhve, heave=12.345, status=A)>",
        )

        i = 0
        raw = 0
        with open(os.path.join(DIRNAME, "furuno_nmea.log"), "rb") as stream:
            nmr = NMEAReader(stream, nmeaonly=False, quitonerror=2)
            for raw, parsed in nmr:
                if raw is not None:
                    # print(f'"{parsed}",')
                    self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                    i += 1
        self.assertEqual(i, 2)

    def testNMEAKENWOOD(self):  # test proprietary Kenwood messages
        EXPECTED_RESULTS = (
            "<NMEA(PKWDWPL, time=15:08:03, status=V, lat=42.619, NS=N, lon=-71.3471666667, EW=W, sog=, cog=, date=2016-03-19, alt=, wpt=test, ts=5)>",
            "<NMEA(PKLDS, time=00:12:35, status=A, lat=35.7444166667, NS=N, lon=139.6698333333, EW=E, sog=15.0, cog=38.8, dat=1998-04-11, declination=10.8, dec_dir=W00, fleet=100.0, senderid=2000, senderstatus=15.0, reserved=0.0)>",
            "<NMEA(PKNDS, time=12:46:40, status=A, lat=49.90243, NS=N, lon=-119.39332, EW=W, sog=0.0, cog=0.0, date=2023-02-12, declination=19.2, dec_dir=W00, senderid=U00002, senderstatus=207.0, reserved=0.0)>",
            "<NMEA(PKLSH, lat=40.0, NS=N, lon=135.0, EW=E, time=02:17:20, status=A, fleetId=100, deviceId=2000)>",
            "<NMEA(PKNSH, lat=40.0, NS=N, lon=135.0, EW=E, time=02:17:20, status=A, senderid=U00001)>",
        )

        i = 0
        raw = 0
        with open(os.path.join(DIRNAME, "kenwood_nmea.log"), "rb") as stream:
            nmr = NMEAReader(stream, nmeaonly=False, quitonerror=2)
            for raw, parsed in nmr:
                if raw is not None:
                    # print(f'"{parsed}",')
                    self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                    i += 1
        self.assertEqual(i, 5)

    def testNMEALOCOSYSGET(self):  # test proprietary Locosys GET messages
        EXPECTED_RESULTS = (
            "<NMEA(PLSVD, velE=1.0, velN=0.0, velD=-16.0, velEdev=16.0, velNdev=15.0, velDdev=13.0)>",
            "<NMEA(PLSR, msgType=SLOPE, value=1, response=OK)>",
            "<NMEA(PLSR, msgType=SLOPE, value=0, response=OK)>",
            "<NMEA(PLSR, msgType=MEMS, value=1, response=OK)>",
            "<NMEA(PLSR, msgType=MEMS, value=0, response=OK)>",
            "<NMEA(PLSR, msgType=ATTIT, value=1, response=OK)>",
            "<NMEA(PLSR, msgType=ATTIT, value=0, response=OK)>",
            "<NMEA(PINVMSTR, value=0)>",
            "<NMEA(PINVMSLOPE, slope=-3.13, altDiff=-0.05, moveDist=0.93, slopeAccu=54.42, altDiffAccu=2.6, moveDistAccu=1.86)>",
            "<NMEA(PINVMIMU, timeSecond=1114.106, accelX=-0.3699, accelY=1.51074, accelZ=9.81383, gyroX=0.67139, gyroY=0.61035, gyroZ=-0.30518)>",
            "<NMEA(PINVMATTIT, roll=-20.652, pitch=32.265, yaw=0.0)>",
        )
        i = 0
        raw = 0
        with open(os.path.join(DIRNAME, "locosys_get_nmea.log"), "rb") as stream:
            nmr = NMEAReader(stream, nmeaonly=False, quitonerror=2)
            for raw, parsed in nmr:
                if raw is not None:
                    # print(f'"{parsed}",')
                    self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                    i += 1
        self.assertEqual(i, 11)

    def testNMEALOCOSYSSET(self):  # test proprietary Locosys SET messages
        EXPECTED_RESULTS = (
            "<NMEA(PINVCRES, value=0)>",
            "<NMEA(PINVCSTR, value=14)>",
            "<NMEA(PLSC, msgType=SLOPE, value=1)>",
            "<NMEA(PLSC, msgType=SLOPE, value=0)>",
            "<NMEA(PLSC, msgType=MEMS, value=1)>",
            "<NMEA(PLSC, msgType=MEMS, value=0)>",
            "<NMEA(PLSC, msgType=ATTIT, value=1)>",
            "<NMEA(PLSC, msgType=ATTIT, value=0)>",
            "<NMEA(PLSC, msgType=VER)>",
        )
        i = 0
        raw = 0
        with open(os.path.join(DIRNAME, "locosys_set_nmea.log"), "rb") as stream:
            nmr = NMEAReader(stream, nmeaonly=False, quitonerror=2, msgmode=SET)
            for raw, parsed in nmr:
                if raw is not None:
                    # print(f'"{parsed}",')
                    self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                    i += 1
        self.assertEqual(i, 9)

    def testNMEASEPX5GET(self):  # test proprietary Sepentrio X5 GET messages
        EXPECTED_RESULTS = (
            "<NMEA(PSSNHRP, msgId=HRP, utc=10:47:51, date=2024-03-23, hdg=23.455, roll=1.954, pitch=0.0125, hdgstd=0.123, rollstd=0.0234, pitchstd=0.03765, sip=11, attmode=0, magvar=4.56453, magvardir=W)>",
            "<NMEA(PSSNTFM, msgId=TFM, utc=10:47:51, heightind=2, usage2122=1021, usage2324=1023, usage252627=1025)>",
            "<NMEA(PSSNSNC, msgId=SNC, rev=0, tim=379359000, week=1840, cdidx_01=1, status_01=2, errcode_01=0, info_01=0)>",
            "<NMEA(PSSNSNC, msgId=SNC, rev=0, tim=379359123, week=1841, cdidx_01=1, status_01=2, errcode_01=0, info_01=0, cdidx_02=2, status_02=3, errcode_02=0, info_02=0)>",
        )
        i = 0
        raw = 0
        with open(os.path.join(DIRNAME, "septentriox5_nmea.log"), "rb") as stream:
            nmr = NMEAReader(stream, nmeaonly=False, quitonerror=2)
            for raw, parsed in nmr:
                if raw is not None:
                    # print(f'"{parsed}",')
                    self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                    i += 1
        self.assertEqual(i, 4)

    def testNMEAGPFMI(self):  # test proprietary Feyman GPFMI IMU GET messages

        def getstatus(status) -> str:

            st = ""
            for key, (desc, _) in FMI_STATUS.items():
                if int(status, 16) & key:
                    st += f"{desc} "
            return st

        EXPECTED_RESULTS = (
            "<NMEA(GPFMI, time=16:02:24.400000, lat=0.0, lon=0.0, alt=0.0, roll=3.0182, pitch=0.0573, yaw=9.99999, hrms=0.17, numSV=12, diffAge=0, navmod=2, status=001C0001)>",
            "<NMEA(GPFMI, time=16:02:24.600000, lat=0.0, lon=0.0, alt=0.0, roll=3.0182, pitch=0.0573, yaw=9.99999, hrms=0.17, numSV=12, diffAge=0, navmod=2, status=001C0001)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.423023, lon=113.193168, alt=45.890494, roll=16.593, pitch=-7.75, yaw=3.888, hrms=0.17, numSV=26, diffAge=5, navmod=2, status=001C0001)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.512547, lon=113.637276, alt=45.767895, roll=-3.523, pitch=-7.218, yaw=9.242, hrms=0.17, numSV=27, diffAge=5, navmod=2, status=001C0001)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.19525, lon=113.882219, alt=45.719773, roll=4.998, pitch=-8.686, yaw=0.927, hrms=0.17, numSV=27, diffAge=3, navmod=2, status=001C0001)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.092634, lon=113.283257, alt=45.018596, roll=8.221, pitch=4.892, yaw=-5.005, hrms=0.17, numSV=26, diffAge=4, navmod=2, status=001C0001)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.254565, lon=113.288853, alt=45.661074, roll=7.074, pitch=3.049, yaw=-4.613, hrms=0.17, numSV=25, diffAge=3, navmod=2, status=001C0001)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.509901, lon=113.138161, alt=45.996202, roll=-3.514, pitch=-5.205, yaw=8.724, hrms=0.17, numSV=27, diffAge=3, navmod=2, status=001C0001)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.76182, lon=113.482807, alt=45.764244, roll=-4.72, pitch=6.391, yaw=-8.178, hrms=0.17, numSV=26, diffAge=2, navmod=2, status=001C0001)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.934536, lon=113.034356, alt=45.252132, roll=16.878, pitch=2.358, yaw=-2.944, hrms=0.17, numSV=27, diffAge=2, navmod=2, status=001C0001)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.639909, lon=113.402712, alt=45.615865, roll=11.508, pitch=9.446, yaw=3.934, hrms=0.17, numSV=27, diffAge=5, navmod=2, status=001C0001)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.269057, lon=113.727968, alt=45.891641, roll=-0.085, pitch=6.887, yaw=-16.113, hrms=0.17, numSV=25, diffAge=2, navmod=2, status=001C0001)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.457734, lon=113.13478, alt=45.028494, roll=6.838, pitch=2.27, yaw=8.636, hrms=0.17, numSV=24, diffAge=4, navmod=2, status=001C0001)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.114631, lon=113.083719, alt=45.146318, roll=6.506, pitch=7.586, yaw=-3.084, hrms=0.17, numSV=26, diffAge=4, navmod=2, status=001C0001)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.561758, lon=113.504337, alt=45.81872, roll=-19.365, pitch=1.583, yaw=-7.598, hrms=0.17, numSV=25, diffAge=3, navmod=2, status=001C0001)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.484163, lon=113.286151, alt=45.117093, roll=-7.733, pitch=3.219, yaw=-12.475, hrms=0.17, numSV=24, diffAge=3, navmod=2, status=001C0001)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.077227, lon=113.853113, alt=45.633862, roll=16.283, pitch=-9.75, yaw=12.718, hrms=0.17, numSV=24, diffAge=5, navmod=2, status=001C0001)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.256628, lon=113.893556, alt=45.736646, roll=-13.055, pitch=-6.64, yaw=5.213, hrms=0.17, numSV=26, diffAge=2, navmod=2, status=001C00E1)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.327387, lon=113.710465, alt=45.119112, roll=-15.582, pitch=0.837, yaw=-8.4, hrms=0.17, numSV=24, diffAge=2, navmod=2, status=001C0001)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.238952, lon=113.301512, alt=45.781582, roll=0.25, pitch=6.982, yaw=-3.916, hrms=0.17, numSV=26, diffAge=4, navmod=2, status=001C0001)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.8632, lon=113.998859, alt=45.163301, roll=5.528, pitch=-2.215, yaw=16.083, hrms=0.17, numSV=24, diffAge=2, navmod=2, status=001A0001)>",
            "<NMEA(GPFMI, time=21:39:37.460000, lat=13.952284, lon=113.441564, alt=45.696884, roll=-12.544, pitch=-3.978, yaw=-2.798, hrms=0.17, numSV=25, diffAge=2, navmod=2, status=001A0001)>",
        )
        EXPECTED_RESULTS2 = (
            "Finit PPSReady SyncReady GnssConnect ",
            "Finit PPSReady SyncReady GnssConnect ",
            "Finit PPSReady SyncReady GnssConnect ",
            "Finit PPSReady SyncReady GnssConnect ",
            "Finit PPSReady SyncReady GnssConnect ",
            "Finit PPSReady SyncReady GnssConnect ",
            "Finit PPSReady SyncReady GnssConnect ",
            "Finit PPSReady SyncReady GnssConnect ",
            "Finit PPSReady SyncReady GnssConnect ",
            "Finit PPSReady SyncReady GnssConnect ",
            "Finit PPSReady SyncReady GnssConnect ",
            "Finit PPSReady SyncReady GnssConnect ",
            "Finit PPSReady SyncReady GnssConnect ",
            "Finit PPSReady SyncReady GnssConnect ",
            "Finit PPSReady SyncReady GnssConnect ",
            "Finit PPSReady SyncReady GnssConnect ",
            "Finit PPSReady SyncReady GnssConnect ",
            "Finit FReset FixRlsStage1 FixRlsStage2 PPSReady SyncReady GnssConnect ",
            "Finit PPSReady SyncReady GnssConnect ",
            "Finit PPSReady SyncReady GnssConnect ",
            "Finit FInitOk SyncReady GnssConnect ",
            "Finit FInitOk SyncReady GnssConnect ",
        )
        i = 0
        raw = 0
        with open(os.path.join(DIRNAME, "feyman_nmea.log"), "rb") as stream:
            nmr = NMEAReader(stream, nmeaonly=False, quitonerror=2)
            for raw, parsed in nmr:
                if raw is not None:
                    # print(f'"{parsed}",')
                    self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                    self.assertEqual(getstatus(parsed.status), EXPECTED_RESULTS2[i])
                    i += 1
        self.assertEqual(i, 22)

    def testBADHDR_FAIL(self):  # invalid header in data with quitonerror = 2
        EXPECTED_ERROR = "Unknown protocol header b'$&'."
        with self.assertRaises(NMEAParseError) as context:
            i = 0
            with open(os.path.join(DIRNAME, "pygpsdata-BADHDR.log"), "rb") as stream:
                ubr = NMEAReader(stream, quitonerror=ERR_RAISE, nmeaonly=True)
                for _, _ in ubr:
                    i += 1
        self.assertTrue(EXPECTED_ERROR in str(context.exception))

    def testBADHDR_LOG(self):  # invalid header in data with quitonerror = 1
        i = 0
        with self.assertLogs(level=ERROR) as log:
            with open(os.path.join(DIRNAME, "pygpsdata-BADHDR.log"), "rb") as stream:
                ubr = NMEAReader(stream, quitonerror=ERR_LOG, nmeaonly=True)
                for raw, parsed in ubr:
                    i += 1
            self.assertEqual(
                ["ERROR:pynmeagps.nmeareader:Unknown protocol header b'$&'."],
                log.output,
            )

    def testBADHDR_IGNORE(self):  # invalid header in data with quitonerror = 0
        i = 0
        with open(os.path.join(DIRNAME, "pygpsdata-BADHDR.log"), "rb") as stream:
            ubr = NMEAReader(stream, quitonerror=ERR_IGNORE, nmeaonly=True)
            for raw, parsed in ubr:
                i += 1
            self.assertEqual(i, 15)

    def testLCCHECKSUM(self):  # lower case checksum bytes
        EXPECTED_RESULTS = (
            "<NMEA(GNRMC, time=10:36:07, status=A, lat=53.450657, NS=N, lon=-102.2404103333, EW=W, spd=0.046, cog=, date=2021-03-06, mv=, mvEW=, posMode=A, navStatus=V)>",
            "<NMEA(GPGSV, numMsg=3, msgNum=1, numSV=11, svid_01=1, elv_01=6.0, az_01=14, cno_01=8, svid_02=12, elv_02=43.0, az_02=207, cno_02=28, svid_03=14, elv_03=6.0, az_03=49, cno_03=, svid_04=15, elv_04=44.0, az_04=171, cno_04=23, signalID=1)>",
            "<NMEA(GNZDA, time=10:36:07, day=6, month=3, year=2021, ltzh=00, ltzn=00)>",
            "<NMEA(GNGBS, time=10:36:07, errLat=15.1, errLon=24.2, errAlt=31.0, svid=, prob=, bias=, stddev=, systemId=, signalId=)>",
            "<NMEA(GNVLW, twd=, twdUnit=N, wd=, wdUnit=N, tgd=0.0, tgdUnit=N, gd=0.0, gdUnit=N)>",
        )
        i = 0
        with open(os.path.join(DIRNAME, "pygpsdata-nmea4lc.log"), "rb") as stream:
            ubr = NMEAReader(stream, quitonerror=ERR_RAISE)
            for raw, parsed in ubr:
                # print(f'"{parsed}",')
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1
            self.assertEqual(i, 5)

    def testuserdefined(self):  # test user-defined payload definition dictionary
        EXPECTED_RESULTS = (
            "<NMEA(U1XYZ, fixutc=10:29:29, lat=44.4506706667, NS=N, lon=-1.24026, EW=W)>",
            "<NMEA(U2ZYX, fixutc=10:38:29, data1=somedata, data2=somemoredata)>",
        )
        USERDEFINED = {
            "XYZ": {"fixutc": TM, "lat": LA, "NS": LAD, "lon": LN, "EW": LND},
            "ZYX": {"fixutc": TM, "data1": ST, "data2": ST},
        }
        i = 0
        with open(os.path.join(DIRNAME, "pygpsdata-userdefined.log"), "rb") as stream:
            ubr = NMEAReader(
                stream, quitonerror=ERR_RAISE, nmeaonly=True, userdefined=USERDEFINED
            )
            for raw, parsed in ubr:
                # print(f'"{parsed}",')
                self.assertEqual(str(parsed), EXPECTED_RESULTS[i])
                i += 1
            self.assertEqual(i, 2)


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
