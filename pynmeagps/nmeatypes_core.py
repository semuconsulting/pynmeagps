# pylint: disable=line-too-long
"""
NMEA Protocol core globals and constants

Created on 4 Mar 2021

While the NMEA 0183 © protocol is proprietary, the information here
has been collated from public domain sources.

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
HX = "HX"  # Hexadecimal Integer
IN = "IN"  # Integer
LA = "LA"  # Latitude value ddmm.mmmmm
LN = "LN"  # Longitude value dddmm.mmmmm
ST = "ST"  # String
TM = "TM"  # Time hhmmss.ss

VALID_TYPES = (CH, DE, DT, HX, IN, LA, LN, ST, TM)

# *****************************************
# THESE ARE THE NMEA V4 PROTOCOL TALKER IDS
# *****************************************
NMEA_TALKERS = {
    "AB": "Independent AIS Base Station",
    "AD": "Dependent AIS Base Station",
    # ***************************************************************
    # Heading Track Controller:
    # ***************************************************************
    "AG": "Heading Track Controller (Autopilot): General",
    "AI": "Mobile Class A or B AIS Station",
    "AP": "Heading Track Controller (Autopilot): Magnetic",
    "AN": "AIS Aids to Navigation Station",
    "AR": "AIS Receiving Station",
    "AS": "AIS Station (ITU_R M1371, (Limited Base Station))",
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
    "DE": "DECCA Navigator",
    "DF": "Direction Finder",
    "DP": "Dynamic Position",
    "DU": "Duplex Repeater Station",
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
    "P": "Proprietary",
    # ***************************************************************
    # Heading Sensors:
    # ***************************************************************
    "HC": "Compass, Magnetic",
    "HE": "Gyro, North Seeking",
    "HF": "Fluxgate",
    "HN": "Gyro, Non-North Seeking",
    # ***************************************************************
    # Other Maritime Instrumentation:
    # ***************************************************************
    "HD": "Hull Door Monitoring",
    "HS": "Hull Stress Monitoring",
    "II": "Integrated Instrumentation",
    "IN": "Integrated Navigation",
    "LC": "Loran C",
    "MP": "Microprocessor  Controller",
    "RA": "Radar and/or Radar Plotting",
    "SA": "Physical Shore AIS Station",
    "SC": "Steering Control System/Device",
    "SD": "Sounder, Depth",
    "SG": "Steering Gear/Steering Engine",
    "SN": "Electronic Positioning System",
    "SS": "Sounder, Scanning",
    "TC": "Track Control System",
    # ***************************************************************
    # Velocity Sensors:
    # ***************************************************************
    "VD": "Doppler",
    "VM": "Speed Log, Water, Magnetic",
    "VR": "Voyage Data Recorder",
    "VW": "Speed Log, Water, Mechanical",
    "WD": "Watertight Door Controller/Monitoring Panel",
    "WI": "Weather Instruments",
    "WL": "Water Level Detection Systems",
    "YX": "Transducer",
    # ***************************************************************
    # Timekeepers:
    # ***************************************************************
    "ZA": "Atomic Clock",
    "ZC": "Chronometer",
    "ZQ": "Quartz",
    "ZV": "Radio Update",
}

# ****************************************************************************
# THESE ARE THE NMEA PROTOCOL CORE MESSAGE IDENTITIES
# Payloads for each of these identities are defined in the nmeatypes_* modules
# ****************************************************************************
NMEA_MSGIDS = {
    # ***************************************************************
    # NMEA Standard message types
    # ***************************************************************
    "AAM": "Waypoint Arrival Alarm",
    # "ALM": "Almanac Data",
    "APA": "Auto Pilot A sentence",  # deprecated
    "APB": "Auto Pilot B sentence",
    "BOD": "Bearing Origin to Destination",
    "BWC": "Bearing using Great Circle route",
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
    "HDG": "Heading, Magnetic, Deviation, Variation",
    "HDM": "Heading, Magnetic",  # deprecated
    "HDT": "Heating, True",
    "MSK": "Send control for a beacon receiver",
    "MSS": "Beacon receiver status information",
    "RLM": "Return Link Message",
    "RMA": "Recommended Loran data",
    "RMB": "Recommended Navigation data for GPS",
    "RMC": "Recommended Minimum data",
    "RTE": "Route message",
    "TRF": "Transit Fix Data",
    "STN": "Multiple Data ID",
    "THS": "TRUE Heading and Status",
    "TXT": "Text Transmission",
    "VBW": "Dual Ground / Water Speed",
    "VLW": "Dual Ground Water Distance",
    "VTG": "Course over ground and Groundspeed",
    # "WCV": "Waypoint closure velocity (Velocity Made Good)",
    "WPL": "Waypoint Location information",
    # "XTC": "Cross track error",
    "XTE": "Measured cross track error",
    "ZDA": "Time and Date",
    # "ZTG": "Zulu (UTC) time and time to go (to destination)",
}
NMEA_MSGIDS_PROP = {
    # ***************************************************************
    # NMEA Proprietary message types
    # ***************************************************************
    # ***************************************************************
    # GARMIN Proprietary message types
    # ***************************************************************
    "GRMB": "DGPS Beacon Information",
    "GRMC": "Set Sensor Configuration information",
    "GRMC1": "Set Additional Sensor Configuration Information",
    "GRME": "Estimated Error Information",
    "GRMF": "GPS Fix Data sentence",
    "GRMH": "Aviation Height and VNAV data",
    "GRMI": "Set Sensor Initialisation Information",
    "GRMM": "MapDatum",
    "GRMO": "Set Output Sentence Enable",
    "GRMT": "Sensor Status Information",
    "GRMV": "3D Velocity Information",
    "GRMW": "Set Additional Waypoint Information",
    "GRMZ": "Altitude",
    # ***************************************************************
    # U-BLOX Proprietary message types
    # ***************************************************************
    "UBX00": "PUBX-POSITION Lat/Long Position Data",
    "UBX03": "PUBX-SVSTATUS Satellite Status",
    "UBX04": "PUBX-TIME Time of Day and Clock Information",
    "UBX05": "Lat/Long Position Data",
    "UBX06": "Lat/Long Position Data",
    "UBX40": "Set NMEA message output rate",
    "UBX41": "PUBX-CONFIG Set Protocols and Baudrate",
    # ***************************************************************
    # Dummy message for testing only
    # ***************************************************************
    "FOO": "Dummy message",
}
