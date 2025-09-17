"""
nmeatyps_decodes.py

NMEA Protocol attribute value decode constants.

From various public domain sources.

Created on 26 Aug 2023

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2021
:license: BSD 3-Clause
"""

FIXTYPE_GGA = QUALITY = {
    0: "NO FIX",
    1: "2D",
    2: "3D",
    3: "N/A",
    4: "RTK FIXED",
    5: "RTK FLOAT",
    6: "DR ONLY",
}
"""GGA quality/fix type values"""

GNSSLIST = {
    0: "GPS",
    1: "SBAS",
    2: "Galileo",
    3: "BeiDou",
    4: "IMES",
    5: "QZSS",
    6: "GLONASS",
    7: "NAVIC",
}
"""GNSS code"""

SYSTEMID = {
    "1": "GPS",
    "2": "GLONASS",
    "3": "Galileo",
    "4": "Beidou",
    "5": "QZSS",
    "6": "NavIC",
}
"""NMEA 4.1 System Identifier - key is systemId"""

SIGNALID = {
    ("1", "1"): "GPS L1C/A2",
    ("1", "6"): "GPS L2 CL",
    ("1", "5"): "GPS L2 CM",
    ("1", "7"): "GPS L5 I",
    ("1", "8"): "GPS L5 Q",
    ("3", "7"): "Galileo E1 B2/C2",
    ("3", "1"): "Galileo E5 aI/aQ",
    ("3", "2"): "Galileo E5 bI/bQ",
    ("4", "1"): "BeiDou B1I D12/D22",
    ("4", "B"): "BeiDou B2I D1/D2",
    ("4", "3"): "BeiDou B1 Cp/Cd",
    ("4", "5"): "BeiDou B2 ap/ad",
    ("5", "1"): "QZSS L1C/A2",
    ("5", "4"): "QZSS L1S",
    ("5", "5"): "QZSS L2 CM",
    ("5", "6"): "QZSS L2 CL",
    ("5", "7"): "QZSS L5 I",
    ("5", "8"): "QZSS L5 Q",
    ("2", "1"): "GLONASS L1 OF",
    ("2", "3"): "GLONASS L2 OF",
    ("6", "1"): "NavIC L5 A",
}
"""Signal Identifier - key is (systemId, signal Id), values are hex strings"""

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
