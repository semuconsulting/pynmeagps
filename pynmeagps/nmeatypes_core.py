# pylint: disable=line-too-long
"""
NMEA Protocol core globals and constants

Created on 4 Mar 2021

:author: semuadmin
"""

NMEAS_HDR = "$G"  # standard NMEA header
NMEAP_HDR = "$P"  # proprietary NMEA header
INPUT = 1
OUTPUT = 0
GET = 0
SET = 1
POLL = 2

GNSSLIST = {
    0: "GPS",
    1: "SBAS",
    2: "Galileo",
    3: "BeiDou",
    4: "IMES",
    5: "QZSS",
    6: "GLONASS",
}

# ***************************************************
# THESE ARE THE NMEA PROTOCOL PAYLOAD ATTRIBUTE TYPES
# ***************************************************
CH = "CH"  # Character
DE = "DE"  # Decimal
DT = "DT"  # Date ddmmyy
HX = "HX"  # Hexadecimal
IN = "NU"  # Integer
LA = "LA"  # Latitude value ddmm.mmmmm
LN = "LN"  # Longitude value dddmm.mmmmm
ST = "ST"  # String
TM = "TM"  # Time hhmmss.ss

VALID_TYPES = (CH, DE, DT, HX, IN, LA, LN, ST, TM)

# **************************************
# THESE ARE THE NMEA PROTOCOL TALKER IDS
# **************************************
NMEA_TALKERS = {
    "AB": "Independent AIS Base Station",
    "AD": "Dependent AIS Base Station",
    # ***************************************************************
    # Heading Track Controller:
    # ***************************************************************
    "AG": "Heading Track Controller (Autopilot): General",
    "AP": "Heading Track Controller (Autopilot): Magnetic",
    "AI": "Mobile Class A or B AIS Station",
    "AN": "AIS Aids to Navigation Station",
    "AR": "AIS Receiving Station",
    "AS": "AIS Station (ITU_R M1371, (“Limited Base Station’)",
    "AT": "AIS Transmitting Station",
    "AX": "AIS Simplex Repeater Station",
    "BI": "Bilge Systems",
    "BN": "Bridge Navigational Watch Alarm System",
    "CA": "Central Alarm Management",
    # ***************************************************************
    # Communications:
    # ***************************************************************
    "CD": "Digital Selective Calling (DSC)",
    "CR": "Data Receiver",
    "CS": "Satellite",
    "CT": "Radio-Telephone (MF/HF)",
    "CV": "Radio-Telephone (VHF)",
    "CX": "Scanning Receiver",
    "DF": "Direction Finder",
    "DU": "Duplex Repeater Station",
    "DP": "Dynamic Position",
    "EC": "Electronic Chart System (ECS)",
    "EI": "Electronic Chart Display & Information System (ECDIS)",
    "EP": "Emergency Position Indicating Beacon (EPIRB)",
    "ER": "Engine Room Monitoring Systems",
    "FD": "Fire Door Controller/Monitoring Point",
    "FE": "Fire Extinguisher System",
    "FR": "Fire Detection Point",
    "FS": "Fire Sprinkler System",
    # ***************************************************************
    # Navigation System Satellite Receivers:
    # ***************************************************************
    "GA": "Galileo Positioning System",
    "GB": "BDS (BeiDou System) ",
    "GI": "NavIC (IRNSS)",
    "GL": "GLONASS Receiver",
    "GN": "Global Navigation Satellite System (GNSS)",
    "GP": "Global Positioning System (GPS)",
    "GQ": "QZSS",
    "PU": "Proprietary UBX",
    # ***************************************************************
    # Heading Sensors:
    # ***************************************************************
    "HC": "Compass, Magnetic",
    "HE": "Gyro, North Seeking",
    "HF": "Fluxgate",
    "HN": "Gyro, Non-North Seeking",
}

# ****************************************************************************
# THESE ARE THE NMEA PROTOCOL CORE MESSAGE IDENTITIES
# Payloads for each of these identities are defined in the nmeatypes_* modules
# ****************************************************************************
NMEA_MSGIDS = {
    # ***************************************************************
    # NMEA Standard message types
    # ***************************************************************
    "DTM": "Datum Reference",
    "GAQ": "Poll Standard Message - Talker ID GA (Galileo)",
    "GBQ": "Poll Standard Message - Talker ID GB (BeiDou)",
    "GBS": "GNSS Satellite Fault Detection",
    "GGA": "Global positioning system fix data",
    "GLL": "Latitude and longitude, with time of position fix and status",
    "GLQ": "Poll Standard Message - Talker ID GL (GLONASS)",
    "GNQ": "Poll Standard Message - Talker ID GN (Any GNSS)",
    "GNS": "GNSS Fix Data",
    "GPQ": "Poll Standard Message - Talker ID GP (GPS, SBAS)",
    "GQQ": "Poll Standard Message - Talker ID GQ (QZSS)",
    "GRS": "GNSS Range Residuals",
    "GSA": "GNSS DOP and Active Satellites",
    "GST": "GNSS Pseudo Range Error Statistics",
    "GSV": "GNSS Satellites in View",
    "RLM": "Return Link Message",
    "RMC": "Recommended Minimum data",
    "THS": "TRUE Heading and Status",
    "TXT": "Text Transmission",
    "VLW": "Dual Ground Water Distance",
    "VTG": "Course over ground and Groundspeed",
    "ZDA": "Time and Date",
    # ***************************************************************
    # NMEA Proprietary message types
    # ***************************************************************
    "PUBX00": "PUBX-POSITION Lat/Long Position Data",
    "PUBX03": "PUBX-SVSTATUS Satellite Status",
    "PUBX04": "PUBX-TIME Time of Day and Clock Information",
    "PUBX05": "Lat/Long Position Data",
    "PUBX06": "Lat/Long Position Data",
    "PUBX40": "Set NMEA message output rate",
    "PUBX41": "PUBX-CONFIG Set Protocols and Baudrate",
    # ***************************************************************
    # Dummy message for testing only
    # ***************************************************************
    "FOO-BAR": "Dummy message",
}
