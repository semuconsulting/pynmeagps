"""
pynmeagps Performance benchmarking utility

Usage (kwargs optional): python3 benchmark.py cycles=10000

Created on 5 Nov 2021

:author: semuadmin
:copyright: SEMU Consulting © 2021
:license: BSD 3-Clause
"""
# pylint: disable=line-too-long

from sys import argv
from datetime import datetime
from platform import version as osver, python_version
from pynmeagps.nmeareader import NMEAReader
from pynmeagps._version import __version__ as nmeaver

NMEAMESSAGES = [
    b"$GNDTM,W84,,0.0,N,0.0,E,0.0,W84*71",
    b"$GNRMC,103607.00,A,5327.03942,N,10214.42462,W,0.046,,060321,,,A,V*0E",
    b"$GPRTE,2,1,c,0,PBRCPK,PBRTO,PTELGR,PPLAND,PYAMBU,PPFAIR,PWARRN,PMORTL,PLISMR*73",
    b"$GNRLM,00000078A9FBAD5,083559.00,3,C45B*06",
    b"$GNVTG,,T,,M,0.046,N,0.085,K,A*32",
    b"$GNGNS,103607.00,5327.03942,N,00214.42462,W,AANN,06,5.88,56.0,48.5,,,V*34",
    b"$GNGGA,103607.00,5327.03942,N,00214.42462,W,1,06,5.88,56.0,M,48.5,M,,*64",
    b"$GNGSA,A,3,23,24,20,12,,,,,,,,,9.62,5.88,7.62,1*0C",
    b"$GNGSA,A,3,66,76,,,,,,,,,,,9.62,5.88,7.62,2*08",
    b"$GNGSA,A,3,,,,,,,,,,,,,9.62,5.88,7.62,3*08",
    b"$GNGSA,A,3,,,,,,,,,,,,,9.62,5.88,7.62,4*0F",
    b"$GPGSV,3,1,11,01,06,014,08,12,43,207,28,14,06,049,,15,44,171,23,1*6B",
    b"$GPGSV,3,2,11,17,32,064,16,19,33,094,,20,20,251,31,21,04,354,,1*63",
    b"$GPGSV,3,3,11,23,27,251,31,24,89,268,26,25,05,223,,1*5A",
    b"$GLGSV,3,1,10,65,07,176,,66,57,223,35,67,42,315,23,68,00,341,29,1*7A",
    b"$GLGSV,3,2,10,75,37,057,,76,78,303,18,77,27,253,21,84,19,018,,B*07",
    b"$GLGSV,3,3,10,85,22,078,,86,01,121,,1*76",
    b"$GAGSV,1,1,00,7*73",
    b"$GBGSV,1,1,02,21,,,15,25,,,28,1*7E",
    b"$GNGLL,5327.03942,N,00214.42462,W,103607.00,A,A*68",
    b"$GNGRS,103607.00,1,-2.1,0.2,2.7,-0.4,,,,,,,,,1,1*53",
    b"$GNGRS,103607.00,1,0.6,5.1,,,,,,,,,,,2,1*52",
    b"$GNGRS,103607.00,1,,,,,,,,,,,,,3,7*57",
    b"$GNGRS,103607.00,1,,,,,,,,,,,,,4,1*56",
    b"$GNGST,103607.00,38,60,38,89,15,24,31*63",
    b"$GNZDA,103607.00,06,03,2021,00,00*7F",
    b"$GNGBS,103607.00,15.1,24.2,31.0,,,,,,*6F",
    b"$GNVLW,,N,,N,0.000,N,0.000,N*44",
    b"$PUBX,00,103607.00,5327.03942,N,00214.42462,W,104.461,G3,29,31,0.085,39.63,-0.007,,5.88,7.62,8.09,6,0,0*69",
    b"$PUBX,03,23,1,-,014,06,08,000,12,U,207,43,28,009,14,-,049,06,,000,15,-,171,44,23,000,17,-,064,32,16,000,19,-,094,33,,000,20,U,251,20,31,038,21,-,354,04,,000,23,U,251,27,31,064,24,U,268,89,26,000,25,-,223,05,,000,48,-,,,15,000,52,-,,,28,013,65,-,176,07,,000,66,U,223,57,35,064,67,-,315,42,23,000,68,-,341,00,29,000,75,-,057,37,,000,76,U,303,78,18,000,77,-,253,27,21,000,84,-,018,19,,000,85,-,078,22,,000,86,-,121,01,,000*02",
]


def progbar(i: int, lim: int, inc: int = 20):
    """
    Display progress bar on console.

    :param int i: iteration
    :param int lim: max iterations
    :param int inc: bar increments (20)
    """

    i = min(i, lim)
    pct = int(i * inc / lim)
    if not i % int(lim / inc):
        print("\u2593" * pct + "\u2591" * (inc - pct), end="\r")


def benchmark(**kwargs) -> float:
    """
    pyubx2 Performance benchmark test.

    :param int cycles: (kwarg) number of test cycles (10,000)
    :returns: benchmark as transactions/second
    :rtype: float
    :raises: UBXStreamError
    """

    cyc = int(kwargs.get("cycles", 10000))
    txnc = len(NMEAMESSAGES)
    txnt = txnc * cyc

    print(
        f"\nOperating system: {osver()}",
        f"\nPython version: {python_version()}",
        f"\npynmeagps version: {nmeaver}",
        f"\nTest cycles: {cyc:,}",
        f"\nTxn per cycle: {txnc:,}",
    )

    start = datetime.now()
    print(f"\nBenchmark test started at {start}")
    for i in range(cyc):
        progbar(i, cyc)
        for msg in NMEAMESSAGES:
            _ = NMEAReader.parse(msg)
    end = datetime.now()
    print(f"Benchmark test ended at {end}.")
    duration = (end - start).total_seconds()
    rate = round(txnt / duration, 2)

    print(
        f"\n{txnt:,} messages processed in {duration:,.3f} seconds = {rate:,.2f} txns/second.\n"
    )

    return rate


def main():
    """
    CLI Entry point.

    args as benchmark() method
    """

    benchmark(**dict(arg.split("=") for arg in argv[1:]))


if __name__ == "__main__":

    main()
