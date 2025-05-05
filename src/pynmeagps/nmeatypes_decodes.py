"""
nmeatyps_decodes.py

NMEA Protocol attribute value decode constants.

From various public domain sources.

Created on 26 Aug 2023

:author: semuadmin
:copyright: SEMU Consulting © 2021
:license: BSD 3-Clause
"""

QUALITY = {
    0: "NO FIX",
    1: "2D",
    2: "3D",
    3: "N/A",
    4: "RTK_FIXED",
    5: "RTK_FLOAT",
    6: "DR_ONLY",
}
"""GGA quality values"""

FMI_STATUS = {
    0x00000001: ("Finit", "Filter uninitialized flag"),
    0x00000002: ("Ready", "Filter convergence completion flag"),
    0x00000004: ("Inaccurate", "Filter convergence is in process"),
    0x00000008: ("TiltReject", "Tilt angle over threshold"),
    0x00000010: ("GnssReject", "RTK data poor quality"),
    0x00000020: ("FReset", "Filter reset flag"),
    0x00000040: ("FixRlsStage1", "Installation angle estimation stage 1"),
    0x00000080: ("FixRlsStage2", "Installation angle estimation stage 2"),
    0x00000100: ("FixRlsStage3", "Installation angle estimation stage 3"),
    0x00000200: ("FixRlsStage4", "Installation angle estimation stage 4"),
    0x00000400: ("FixRlsOK", "Installation angle estimation complete"),
    0x00002000: ("Direction1", "Shake RTK pole to initialize direction 1"),
    0x00004000: ("Direction2", "Shake RTK pole to initialize direction 2"),
    0x00010000: ("GnssLost", "Invalid RTK data or RTK data missing"),
    0x00020000: ("FInitOk", "Filter initialization completed"),
    0x00040000: ("PPSReady", "PPS signal detected"),
    0x00080000: ("SyncReady", "Module time synchronized with PPS"),
    0x00100000: ("GnssConnect", "Serial connection with RTK established"),
}
"""GPFMI status values"""
