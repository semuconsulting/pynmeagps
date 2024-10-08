# pylint: disable=line-too-long
"""
NMEA Protocol core globals and constants

Created on 4 Mar 2021

While the NMEA 0183 © protocol is proprietary, the information here
has been collated from public domain sources.

:author: semuadmin
"""

from datetime import datetime

INPUT = 1
"""Input message type"""
OUTPUT = 0
"""Output message type"""
GET = 0
"""GET (receive, response) message types"""
SET = 1
"""SET (command) message types"""
POLL = 2
"""POLL (query) message types"""
SETPOLL = 3
"""SETPOLL (SET or POLL) message types"""
VALNONE = 0
"""Do not validate checksum or msgid"""
VALCKSUM = 1
"""Validate checksum"""
VALMSGID = 2
"""Validate message id"""
NMEA_PROTOCOL = 1
"""NMEA Protocol"""
UBX_PROTOCOL = 2
"""UBX Protocol"""
RTCM3_PROTOCOL = 4
"""RTCM3 Protocol"""
ERR_RAISE = 2
"""Raise error and quit"""
ERR_LOG = 1
"""Log errors"""
ERR_IGNORE = 0
"""Ignore errors"""
DEF_STND = 0
"""Standard message definition"""
DEF_PROP = 1
"""Proprietary message definition"""
DEF_USER = 2
"""User-defined message definition"""
DEF_UNKN = 3
"""Unknown (not public domain) message definition"""

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
FIXTYPE_GGA = {
    0: "NO FIX",
    1: "3D",
    2: "3D",
    4: "RTK FIXED",
    5: "RTK FLOAT",
    6: "DR",
}
"""Fix type from GGA"""

GPSEPOCH0 = datetime(1980, 1, 6)
"""GPS epoch base date"""
# Geodetic datum spheroid values:
# WGS84, ETRS89, EPSG4326
WGS84 = "WGS_84"
"""WGS84 datum descriptor"""
WGS84_SMAJ_AXIS = 6378137.0  # semi-major axis
"""WGS84 semi-major axis"""
WGS84_FLATTENING = 298.257223563  # flattening
"""WGS84 flattening"""

# ***************************************************
# THESE ARE THE NMEA PROTOCOL PAYLOAD ATTRIBUTE TYPES
# ***************************************************
CH = "CH"  # Character
DE = "DE"  # Decimal
DT = "DT"  # Date ddmmyy
DTL = "DTL"  # Date ddmmyyyy
DM = "DM"  # Date mmddyy
HX = "HX"  # Hexadecimal Integer
IN = "IN"  # Integer
LA = "LA"  # Latitude value ddmm.mmmmm (ddmm.mmmmmmm in HP mode)
LAD = "LAD"  # Latitude direction (N/S)
LN = "LN"  # Longitude value dddmm.mmmmm (dddmm.mmmmmmm in HP mode)
LND = "LND"  # Longitude direction (E/W)
ST = "ST"  # String
TM = "TM"  # Time hhmmss.ss

VALID_TYPES = (CH, DE, DM, DT, DTL, HX, IN, LA, LAD, LN, LND, ST, TM)

# *****************************************
# THESE ARE THE NMEA V4 PROTOCOL TALKER IDS
# *****************************************
NMEA_TALKERS = {
    # ***************************************************************
    # Base Stations:
    # ***************************************************************
    "AB": "Independent AIS Base Station",
    "AD": "Dependent AIS Base Station",
    # ***************************************************************
    # Heading Track Controllers:
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
    "GB": "BDS (BeiDou System)",
    "BD": "BDS (BeiDou System)",  # legacy, use GB instead
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
    "IC": "Integrated Communications System",
    "II": "Integrated Instrumentation",
    "IN": "Integrated Navigation",
    "LC": "Loran C",
    "MP": "Microprocessor  Controller",
    "ND": "Network Device",
    "NL": "Navigation Light Controller",
    "RA": "Radar and/or Radar Plotting",
    "RC": "Propulsion Machinery including Remote Control",
    "SA": "Physical Shore AIS Station",
    "SC": "Steering Control System/Device",
    "SD": "Sounder, Depth",
    "SG": "Steering Gear/Steering Engine",
    "SI": "Serial to Network Gateway Function",
    "SN": "Electronic Positioning System",
    "SS": "Sounder, Scanning",
    "TC": "Track Control System",
    "TI": "Turn Rate Indicator",
    "UP": "Microprocessor Controller",
    "U0": "User-configured talker identifier",
    "U1": "User-configured talker identifier",
    "U2": "User-configured talker identifier",
    "U3": "User-configured talker identifier",
    "U4": "User-configured talker identifier",
    "U5": "User-configured talker identifier",
    "U6": "User-configured talker identifier",
    "U7": "User-configured talker identifier",
    "U8": "User-configured talker identifier",
    "U9": "User-configured talker identifier",
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
"""Recognised NMEA Talkers."""

# format list of permissible NMEA 2-byte header sequences
NMEA_HDR = {b"\x24" + i[0:1].encode("utf-8") for i in NMEA_TALKERS}

# ****************************************************************************
# THESE ARE THE NMEA PROTOCOL CORE MESSAGE IDENTITIES
# Payloads for each of these identities are defined in the nmeatypes_* modules
# Commented-out entries are those which have not yet been implemented,
# principally because no public domain definition has yet been identified.
# Full specifications can be found in NMEA 0183—v4.30, IEC 61162-1:2024.
# ****************************************************************************
NMEA_MSGIDS = {
    "AAM": "Waypoint arrival alarm",
    "ABK": "AIS addressed and binary broadcast acknowledgement",
    "ABM": "AIS addressed binary and safety related message",
    "ACA": "AIS channel assignment message",
    "ACK": "Acknowledge alarm",
    "ACN": "Alert Command",
    "ACS": "AIS channel management information source",
    # "AGL": "Alert Group List",
    "AIR": "AIS interrogation request",
    "AKD": "Acknowledge detail alarm condition7",
    "ALA": "Report detailed alarm condition",
    "ALC": "Cyclic alert list",
    "ALF": "Alert sentence",
    "ALR": "Set alarm state",
    "APA": "Auto Pilot A sentence",  # deprecated
    "APB": "Heading/track controller (autopilot) sentence",
    "ARC": "Alert command refused",
    "BBM": "AIS broadcast binary message",
    "BEC": "Bearing and distance to waypoint - Dead reckoning",
    "BOD": "Bearing origin to destination",
    "BWC": "Bearing and distance to waypoint - Great circle",
    "BWR": "Bearing and distance to waypoint - Rhumb line",
    "BWW": "Bearing waypoint to waypoint",
    "CUR": "Water current layer - Multi-layer water current data",
    "DBT": "Depth below transducer",
    "DDC": "Display dimming control",
    "DOR": "Door status detection",
    "DPT": "Depth",
    "DSC": "Digital selective calling information",
    "DSE": "Expanded digital selective calling",
    "DTM": "Datum reference",
    "EPV": "Command or report equipment property value",
    "ETL": "Engine telegraph operation status",
    "EVE": "General event message",
    "FIR": "Fire detection",
    "FSI": "Frequency set information",
    "GAQ": "Poll Standard Message - Talker ID GA (Galileo)",
    "GBQ": "Poll Standard Message - Talker ID GB (BeiDou)",
    "GBS": "GNSS satellite fault detection",
    "GEN": "Generic binary information",
    "GFA": "GNSS fix accuracy and integrity",
    "GGA": "Global positioning system fix data",
    "GLL": "Geographic position - Latitude/longitude",
    "GLQ": "Poll Standard Message - Talker ID GL (GLONASS)",
    "GMP": "GNSS Map Projection Fix Data",
    "GNQ": "Poll Standard Message - Talker ID GN (Any GNSS)",
    "GNS": "GNSS Fix Data",
    "GPQ": "Poll Standard Message - Talker ID GP (GPS, SBAS)",
    "GQQ": "Poll Standard Message - Talker ID GQ (QZSS)",
    "GRS": "GNSS range residuals",
    "GSA": "GNSS DOP and active satellites",
    "GST": "GNSS pseudorange noise statistics",
    "GSV": "GNSS satellites in view",
    "HBT": "Heartbeat supervision sentence",
    "HCR": "Heading correction report",
    "HDG": "Heading, deviation and variation",
    "HDM": "Heading, Magnetic",  # deprecated
    "HDT": "Heading true",
    "HMR": "Heading monitor receive",
    "HMS": "Heading monitor set",
    "HRM": "heel angle, roll period and roll amplitude measurement device",
    "HSC": "Heading steering command",
    "HSS": "Hull stress surveillance systems",
    "HTC": "Heading/track control command",
    "HTD": "Heading /track control",
    "LLQ": "Leica local position and quality",
    "LR1": "AIS long-range reply sentence 1",
    "LR2": "AIS long-range reply sentence 2",
    "LR3": "AIS long-range reply sentence 3",
    "LRF": "AIS long-range function",
    "LRI": "AIS long-range interrogation",
    "MOB": "Man over board notification",
    "MSK": "MSK receiver interface",
    "MSS": "MSK receiver signal status",
    "MTW": "Water temperature",
    "MWD": "Wind direction and speed",
    "MWV": "Wind speed and angle",
    "NAK": "Negative acknowledgement",
    "NRM": "NAVTEX receiver mask",
    "NRX": "NAVTEX received message",
    "NSR": "Navigation status report",
    "OSD": "Own ship data",
    "POS": "Device position and ship dimensions report or configuration",
    "PRC": "Propulsion remote control status",
    "RLM": "Return link message",
    "RMA": "Recommended minimum specific LORAN-C data",
    "RMB": "Recommended minimum navigation information",
    "RMC": "Recommended minimum specific GNSS data",
    "ROR": "Rudder order status",
    "ROT": "Rate of turn",
    "RRT": "Report route transfer",
    "RPM": "Revolutions",
    "RSA": "Rudder sensor angle",
    "RSD": "Radar system data",
    "RTE": "Routes",
    "SFI": "Scanning frequency information",
    "SM1": "SafetyNET Message, All Ships/NavArea",
    "SM2": "SafetyNET Message, Coastal Warning Area",
    "SM3": "SafetyNET Message, Circular Area address",
    "SM4": "SafetyNET Message, Rectangular Area Address",
    "SMB": "IMO SafetyNET Message Body",
    "SPW": "Security password sentence",
    "SSD": "AIS ship static data",
    "STN": "Multiple data ID",
    "THS": "True heading and status",
    "TLB": "Target label",
    "TLL": "Target latitude and longitude",
    "TRC": "Thruster control data",
    "TRL": "AIS transmitter-non-functioning log",
    "TRD": "Thruster response data",
    "TRF": "Transit Fix Data",  # deprecated
    "TTD": "Tracked target data",
    "TTM": "Tracked target message",
    "TUT": "Transmission of multi-language text",
    "TXT": "Text transmission",
    "UID": "User identification code transmission",
    "VBW": "Dual ground/water speed",
    "VDM": "AIS VHF data-link message",
    "VDO": "AIS VHF data-link own-vessel report",
    "VDR": "Set and drift",
    "VER": "Version",
    "VHW": "Water speed and heading",
    "VLW": "Dual ground/water distance",
    "VPW": "Speed measured parallel to wind",
    "VSD": "AIS voyage static data",
    "VTG": "Course over ground and ground speed",
    "WAT": "Water level detection",
    "WCV": "Waypoint closure velocity",
    "WNC": "Distance waypoint to waypoint",
    "WPL": "Waypoint location",
    "XDR": "Transducer measurements",
    "XTE": "Cross-track error, measured",
    "XTR": "Cross-track error, dead reckoning",
    "ZDA": "Time and date",
    "ZDL": "Time and distance to variable point",
    "ZFO": "UTC and time from origin waypoint",
    "ZTG": "UTC and time to destination waypoint",
    # ***************************************************************
    # Dummy message for testing only
    # ***************************************************************
    "FOO": "Dummy message",
}
"""
Recognised Standard NMEA Message Identifiers.

Payload definitions for standard GET messages are defined in 
`NMEA_PAYLOADS_GET`. Standard POLL messages are defined in
`NMEA_PAYLOADS_POLL`.
"""

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
    # JVC Kenwood Proprietary message types
    # ***************************************************************
    "KLDS": "Position, Speed, Course",
    "KLSH": "FleetSync GNSS sentence",
    "KNDS": "Position, Speed, Course",
    "KNSH": "Position",
    "KWDWPL": "Waypoint Location",
    # ***************************************************************
    # Magellan Proprietary message types
    # ***************************************************************
    "MGNWPL": "Waypoint Location",
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
    "ASHR": "RT300 Roll and Pitch",
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
    # "ASHRHR": "Proprietary Roll and Pitch",
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
    # Furuno
    # ***************************************************************
    "FECGPATT": "Attitude yaw, pitch, roll",
    "FECGPHVE": "Heave",
    # ***************************************************************
    # Locosys Proprietary Messages (GET and SET)
    # ***************************************************************
    "INVCRES": "Clear the NVM data",
    "INVCSTR": "Start session",
    "INVMATTIT": "ATTIT information",
    "INVMIMU": "MEMS RAW-DATA message information",
    "INVMINR": "Calibration status",
    "INVMSTR": "Session Status",
    "INVMSLOPE": "SLOPE information",
    "LSC": "Set status/poll version",
    "LSR": "Set status response",
    "LSVD": "Attitude yaw, pitch, roll",
    # "MTKnnn": "Proprietary command sets - not implemented",
}
"""
Recognised Proprietary NMEA Message Identifiers.

Payload definitions for proprietary GET messages are defined in 
`NMEA_PAYLOADS_GET_PROP`. Proprietary SET and POLL messages are defined
in `NMEA_PAYLOADS_SET` and `NMEA_PAYLOADS_POLL`.
"""

NMEA_PREFIX_PROP = ("FEC", "UBX", "TNL", "ASHR", "GPPADV")
"""
Proprietary NMEA Message Prefixes where `msgId` is part of payload.

For proprietary messages with these prefixes, the `msgId` is defined as
the first element of the payload. The unique payload dictionary key is
therefore a combination of `prefix` + `msgId`.

NB: There are some exceptions which require special handling e.g. `PASHR`.
"""
