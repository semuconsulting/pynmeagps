# pylint: disable=line-too-long
"""
NMEA Protocol core globals and constants

Created on 4 Mar 2021

While the NMEA 0183 © protocol is proprietary, the information here
has been collated from public domain sources.

:author: semuadmin
"""

from datetime import datetime

NMEA_HDR = [b"\x24\x47", b"\x24\x50"]  # standard, proprietary
INPUT = 1
OUTPUT = 0
GET = 0
SET = 1
POLL = 2
VALNONE = 0
VALCKSUM = 1
VALMSGID = 2
ERR_IGNORE = 0
ERR_LOG = 1
ERR_RAISE = 2
# proprietary messages where msgId is first element of payload:
PROP_MSGIDS = ("UBX", "TNL", "ASHR", "GPPADV")

GNSSLIST = {
    0: "GPS",
    1: "SBAS",
    2: "Galileo",
    3: "BeiDou",
    4: "IMES",
    5: "QZSS",
    6: "GLONASS",
}

GPSEPOCH0 = datetime(1980, 1, 6)
# Geodetic datum spheroid values:
# WGS84, ETRS89, EPSG4326
WGS84 = "WGS_84"
WGS84_SMAJ_AXIS = 6378137.0  # semi-major axis
WGS84_FLATTENING = 298.257223563  # flattening

# ***************************************************
# THESE ARE THE NMEA PROTOCOL PAYLOAD ATTRIBUTE TYPES
# ***************************************************
CH = "CH"  # Character
DE = "DE"  # Decimal
DT = "DT"  # Date ddmmyy
DM = "DM"  # Date mmddyy
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
    "GMP": "GNSS Map Projection Fix Data",
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
    "LLQ": "Leica local position and quality",
    "MSK": "Send control for a beacon receiver",
    "MSS": "Beacon receiver status information",
    "RLM": "Return Link Message",
    "RMA": "Recommended Loran data",
    "RMB": "Recommended Navigation data for GPS",
    "RMC": "Recommended Minimum data",
    "ROT": "Rate and direction of turn",
    "RTE": "Route message",
    "STN": "Multiple Data ID",
    "THS": "True Heading and Status",
    "TRF": "Transit Fix Data",
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
    # JVCKenwood Proprietary message types
    # ***************************************************************
    "KLSH": "FleetSync GNSS sentence",
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
    # Trimble Proprietary message types
    # ***************************************************************
    "ASHRALR": "Alarms",
    "ASHRARA": "True Heading",
    "ASHRARR": "Vector & Accuracy",
    "ASHRATT": "True Heading",
    "ASHRBTS": "Bluetooth Status",
    "ASHRCAP": "Parameters of Antenna Used at Received Base",
    "ASHRCPA": "Height of Antenna Used at Received Base",
    "ASHRCPO": "Position of Received Base",
    "ASHRDDM": "Differential Decoder Message",
    "ASHRDDS": "Differential Decoder Status",
    "ASHRHPR": "True Heading",
    "ASHRHR": "Proprietary Roll and Pitch",
    "ASHRLTN": "Latency",
    "ASHRMDM": "Modem State and Parameter",
    "ASHRPOS": "Position",
    "ASHRPBN": "Position and Velocity Information",
    "ASHRPTT": "PPS Time Tag",
    "ASHRPWR": "Power Status",
    "ASHRRCS": "Recording Status",
    "ASHRSBD": "BEIDOU Satellites Status",
    "ASHRSGA": "GALILEO Satellites Status (E1,E5a,E5b)",
    "ASHRSGL": "GLONASS Satellites Status",
    "ASHRSGO": "GALILEO Satellites Status (E1,E5a,E5b,E6)",
    "ASHRSGP": "GPS Satellites Status",
    "ASHRSIR": "IRNSS Satellites Status",
    "ASHRSLB": "L-Band Satellites Status",
    "ASHRSQZ": "QZSS Satellites Status",
    "ASHRSSB": "SBAS Satellites Status",
    "ASHRTEM": "Receiver Temperature",
    "ASHRTHS": "True Heading and Status",
    "ASHRTTT": "Event Marker",
    "ASHRVCR": "Vector and Accuracy",
    "ASHRVCT": "Vector and Accuracy",
    "ASHRVEL": "Velocity",
    "FUGDP": "Fugro Dynamic Positioning",
    "GPPADV110": "Position and satellite information for RTK network operations 110",
    "GPPADV120": "Position and satellite information for RTK network operations 120",
    "TNLAVR": "Time, yaw, tilt/roll, range for moving baseline RTK",
    "TNLBPQ": "Base station position and quality indicator",
    "TNLDG": "L-band corrections and beacon signal strength and related information",
    "TNLEVT": "Event marker data",
    "TNLGGK": "Time, position, position type, DOP",
    "TNLGGKx": "GNSS Position Message",
    "TNLPJK": "Local coordinate position output",
    "TNLPJT": "Projection type",
    "TNLREX": "Rover Extended Output",
    "TNLVGK": "Vector information",
    "TNLVHD": "Heading information",
    # ***************************************************************
    # Dummy message for testing only
    # ***************************************************************
    "FOO": "Dummy message",
}
