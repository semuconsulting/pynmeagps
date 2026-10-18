"""
pynmeagps Performance benchmarking utility

Usage (kwargs optional): python3 benchmark.py cycles=10000

Created on 5 Nov 2021

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2021
:license: BSD 3-Clause
"""

# pylint: disable=line-too-long

from io import BytesIO
import os
import sys
from time import process_time_ns
from platform import version as osver, python_version
from pynmeagps.nmeareader import NMEAReader as reader
from pynmeagps._version import __version__ as pgmver

# get path to site-packages (source) folder within venv
pypath = (
    f"{os.path.expanduser('~')}/pygpsclient/lib/python"
    f"{sys.version_info.major}.{sys.version_info.minor}/site-packages"
)
sys.path.insert(0, os.path.abspath(pypath))

CYAN = "\033[1m\033[36m"
NORM = "\033[0m"
TESTDATA = [
    b"$GNDTM,W84,,0.0,N,0.0,E,0.0,W84*71\r\n",
    b"$GNRMC,103607.00,A,5327.03942,N,10214.42462,W,0.046,,060321,,,A,V*0E\r\n",
    b"$GPRTE,2,1,c,0,PBRCPK,PBRTO,PTELGR,PPLAND,PYAMBU,PPFAIR,PWARRN,PMORTL,PLISMR*73\r\n",
    b"$GNRLM,00000078A9FBAD5,083559.00,3,C45B*06\r\n",
    b"$GNVTG,,T,,M,0.046,N,0.085,K,A*32\r\n",
    b"$GNGNS,103607.00,5327.03942,N,00214.42462,W,AANN,06,5.88,56.0,48.5,,,V*34\r\n",
    b"$GNGGA,103607.00,5327.03942,N,00214.42462,W,1,06,5.88,56.0,M,48.5,M,,*64\r\n",
    b"$GNGSA,A,3,23,24,20,12,,,,,,,,,9.62,5.88,7.62,1*0C\r\n",
    b"$GNGSA,A,3,66,76,,,,,,,,,,,9.62,5.88,7.62,2*08\r\n",
    b"$GNGSA,A,3,,,,,,,,,,,,,9.62,5.88,7.62,3*08\r\n",
    b"$GNGSA,A,3,,,,,,,,,,,,,9.62,5.88,7.62,4*0F\r\n",
    b"$GPGSV,3,1,11,01,06,014,08,12,43,207,28,14,06,049,,15,44,171,23,1*6B\r\n",
    b"$GPGSV,3,2,11,17,32,064,16,19,33,094,,20,20,251,31,21,04,354,,1*63\r\n",
    b"$GPGSV,3,3,11,23,27,251,31,24,89,268,26,25,05,223,,1*5A\r\n",
    b"$GLGSV,3,1,10,65,07,176,,66,57,223,35,67,42,315,23,68,00,341,29,1*7A\r\n",
    b"$GLGSV,3,2,10,75,37,057,,76,78,303,18,77,27,253,21,84,19,018,,B*07\r\n",
    b"$GLGSV,3,3,10,85,22,078,,86,01,121,,1*76\r\n",
    b"$GAGSV,1,1,00,7*73\r\n",
    b"$GBGSV,1,1,02,21,,,15,25,,,28,1*7E\r\n",
    b"$GNGLL,5327.03942,N,00214.42462,W,103607.00,A,A*68\r\n",
    b"$GNGRS,103607.00,1,-2.1,0.2,2.7,-0.4,,,,,,,,,1,1*53\r\n",
    b"$GNGRS,103607.00,1,0.6,5.1,,,,,,,,,,,2,1*52\r\n",
    b"$GNGRS,103607.00,1,,,,,,,,,,,,,3,7*57\r\n",
    b"$GNGRS,103607.00,1,,,,,,,,,,,,,4,1*56\r\n",
    b"$GNGST,103607.00,38,60,38,89,15,24,31*63\r\n",
    b"$GNZDA,103607.00,06,03,2021,00,00*7F\r\n",
    b"$GNGBS,103607.00,15.1,24.2,31.0,,,,,,*6F\r\n",
    b"$GNVLW,,N,,N,0.000,N,0.000,N*44\r\n",
    b"$PUBX,00,103607.00,5327.03942,N,00214.42462,W,104.461,G3,29,31,0.085,39.63,-0.007,,5.88,7.62,8.09,6,0,0*69\r\n",
    b"$PUBX,03,23,1,-,014,06,08,000,12,U,207,43,28,009,14,-,049,06,,000,15,-,171,44,23,000,17,-,064,32,16,000,19,-,094,33,,000,20,U,251,20,31,038,21,-,354,04,,000,23,U,251,27,31,064,24,U,268,89,26,000,25,-,223,05,,000,48,-,,,15,000,52,-,,,28,013,65,-,176,07,,000,66,U,223,57,35,064,67,-,315,42,23,000,68,-,341,00,29,000,75,-,057,37,,000,76,U,303,78,18,000,77,-,253,27,21,000,84,-,018,19,,000,85,-,078,22,,000,86,-,121,01,,000*02\r\n",
]
msgb = b""
for msg in TESTDATA:
    msgb += msg
BYTESTREAM = msgb


def progbar(i: int, lim: int, inc: int = 50):
    """
    Display progress bar on console.

    :param int i: iteration
    :param int lim: max iterations
    :param int inc: bar increments (50)
    """

    i = min(i, lim)
    pct = int(i * inc / lim)
    if not i % int(lim / inc):
        print(
            f"{int(pct*100/inc):02}% " + "\u2593" * pct + "\u2591" * (inc - pct),
            end="\r",
        )


def benchmark(**kwargs) -> tuple[float,float]:
    """
    pyrtcm Performance benchmark test.

    :param int cycles: (kwarg) number of test cycles (10,000)
    :returns: benchmark as transactions/second
    :rtype: tuple[float,float]
    :raises: StreamError
    """

    cyc = int(kwargs.get("cycles", 5000))
    txnc = len(TESTDATA)
    txnt = txnc * cyc

    print(
        f"\nAbsolute path: {CYAN}{pypath}{NORM}",
        f"\nOperating system: {CYAN}{osver()}{NORM}",
        f"\nPython version: {CYAN}{python_version()}{NORM}",
        f"\nProgram version: {CYAN}{pgmver}{NORM}",
        f"\nTest cycles: {CYAN}{cyc:,}{NORM}",
        f"\nTxn per cycle: {CYAN}{txnc:,}{NORM}",
    )

    start = process_time_ns()
    bar = 50
    print(f"\nBenchmark test started at {start}")
    for i in range(cyc):
        progbar(i, cyc, bar)
        stream = BytesIO(BYTESTREAM)
        sbr = reader(stream)
        for _, _ in sbr:
            pass
    end = process_time_ns()
    print(f"Benchmark test ended at {end}{' ' * (bar-20)}")
    duration = end - start
    msglen = len(BYTESTREAM) * cyc
    txs = round(txnt * 1e9 / duration, 2)
    kbs = round(msglen * 1e9 / duration / 2**10, 2)

    print(
        f"\n{txnt:,} messages processed in {duration/1e9:,.3f} seconds = "
        f"{CYAN}{txs:,.2f}{NORM} txns/second, {CYAN}{kbs:,.2f}{NORM} kB/second ({CYAN}{kbs*8000:,.0f}{NORM} baud).\n"
    )

    return txs, kbs


def main():
    """
    CLI Entry point.

    args as benchmark() method
    """

    benchmark(**dict(arg.split("=") for arg in sys.argv[1:]))


if __name__ == "__main__":
    main()
