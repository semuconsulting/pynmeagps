# pylint: disable=line-too-long
"""
NMEA Protocol core globals and constants

Created on 4 Mar 2021

While the NMEA 0183 © protocol is proprietary, the information here
has been collated from public domain sources.

:author: semuadmin (Steve Smith)
"""

# pylint: disable=fixme

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
DEFAULT_BUFSIZE = 4096
"""Default socket buffer size"""
ENCODE_NONE = 0
"""No socket encoding"""
ENCODE_CHUNKED = 1
"""chunked socket encoding"""
ENCODE_GZIP = 2
"""gzip socket encoding"""
ENCODE_COMPRESS = 4
"""compress socket encoding"""
ENCODE_DEFLATE = 8
"""deflate socket encoding"""

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
QS = "QS"  # Quectel status (R/W/OK/ERROR)
ST = "ST"  # String
TM = "TM"  # Time hhmmss.ss

VALID_TYPES = (CH, DE, DM, DT, DTL, HX, IN, LA, LAD, LN, LND, QS, ST, TM)

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
    "FMI": "Feyman IMU roll, pitch, yaw",
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
    # Quectel PAIR Proprietary message types LC29 etc.
    # ***************************************************************
    "AIR001": "Ack",
    "AIR002": "GNSS Subsys Power On",
    "AIR003": "GNSS Subsys Power Off",
    "AIR004": "GNSS Subsys Hot Start",
    "AIR005": "GNSS Subsys Warm Start",
    "AIR006": "GNSS Subsys Cold Start",
    "AIR007": "GNSS Subsys Full Cold Start",
    "AIR010": "Request Aiding",
    # "AIR011": "Unknown definition",  # TODO
    # "AIR020": "Get firmware release information",  # TODO
    "AIR050": "Common Set Fix Rate",
    "AIR051": "Common Get Fix Rate",
    "AIR058": "Common Set Min Snr",
    "AIR059": "Common Get Min Snr",
    "AIR062": "Common Set NMEA Output Rate",
    "AIR063": "Common Get NMEA Output Rate",
    "AIR066": "Common Set GNSS Search Mode",
    "AIR067": "Common Get GNSS Search Mode",
    "AIR070": "Common Set Static Threshold",
    "AIR071": "Common Get Static Threshold",
    "AIR072": "Common Set Elev Mask",
    "AIR073": "Common Get Elev Mask",
    "AIR074": "Common Set AIC Enable",
    "AIR075": "Common Get AIC Status",
    "AIR080": "Common Set Navigation Mode",
    "AIR081": "Common Get Navigation Mode",
    "AIR086": "Common Set Debuglog Output",
    "AIR087": "Common Get Debuglog Output",
    "AIR100": "Common Set Nmea Output Mode",
    "AIR101": "Common Get Nmea Output Mode",
    "AIR104": "Common Set Dual Band",
    "AIR105": "Common Get Dual Band",
    # "AIR161": "Force standby mode",  # TODO
    # "AIR351": "Support QZSS NMEA",  # TODO
    "AIR382": "Test Lock System Sleep",
    "AIR391": "Test Jamming Detect",
    "AIR400": "DGPS Set Mode",
    "AIR401": "DGPS Get Mode",
    "AIR410": "SBAS Enable",
    "AIR411": "SBAS Get Status",
    "AIR420": "SLAS Enable",
    "AIR421": "SLAS Get Status",
    "AIR432": "RTCM Set Output Mode",
    "AIR433": "RTCM Get Output Mode",
    "AIR434": "RTCM Set Output Ant Pnt",
    "AIR435": "RTCM Get Output Ant Pnt",
    "AIR436": "RTCM Set Output Ephemeris",
    "AIR437": "RTCM Get Output Ephemeris",
    "AIR490": "Set EASYTM status",
    "AIR491": "Get EASY status",
    # "AIR496": "EPOC Enable", # TODO
    # "AIR498": "EPOC Set Config",# TODO
    # "AIR507": "EPOC Clear Data",# TODO
    # "AIR508": "EPOC Get Status",# TODO
    # "AIR509":"EPOC Get Prediction Status", # TODO
    "AIR511": "NVRAM Save Navigation Data",
    "AIR512": "NVRAM Clear Navigation Data",
    "AIR513": "NVRAM Save Setting",
    "AIR6010": "DR Set Custom Message Output",
    "AIR6011": "DR Get Custom Message Output",
    "AIR650": "Low Power Entry Rtc Mode",
    # "AIR690": "Enter periodic mode for power saving",  # TODO
    # "AIR751": "Fix NMEA output time behind PPS",  # TODO
    "AIR752": "PPS Set Config Cmd",
    # "AIR820": "Set LOCUS logging status",  # TODO
    # "AIR821": "Get LOCUS logging status",  # TODO
    # "AIR824": "Erase LOCUS logger flash",  # TODO
    # "AIR826": "Dump LOCUS flash data",  # TODO
    "AIR864": "IO Set Baudrate",
    "AIR865": "IO Get Baudrate",
    "AIR866": "IO Set Flow Control",
    "AIR867": "IO Get Flow Control",
    "AIRSPF": "Jamming status L1",
    "AIRSPF5": "Jamming status L5",
    # ***************************************************************
    # Quectel PQTM Proprietary message types LG290P/LG580P
    # ***************************************************************
    "QTMANTENNASTATUS": "Report Antenna Status",
    "QTMBKP": "Set Backup Mode",
    "QTMCFGAIC": "Sets/Gets AIC Function",
    "QTMCFGANTDELTA": "Sets/Gets Delta Between Ref Point and Antenna",
    "QTMCFGANTINF": "Sets/Gets Antenna Information",
    "QTMCFGBLD": "Sets/Gets Baseline Between Two Antennas",
    "QTMCFGCNST": "Sets/Gets Constellation Configuration",
    "QTMCFGDR": "Sets/Gets DR State",
    "QTMCFGDRHOT": "Sets/Gets DR Hot Start Feature",
    "QTMCFGDRRTD": "Sets/Gets DR Running TIme and Distance",
    "QTMCFGEINSMSG": "Sets/Gets INS, IMU, GPS Status",
    "QTMCFGELETHD": "Sets/Gets Elevation Threshold for Position Engine",
    "QTMCFGFIXRATE": "Sets/Gets Fix Interval",
    "QTMCFGGEOFENCE": "Sets/Gets Geofence Feature",
    "QTMCFGGEOSEP": "Sets/Gets Geoidal Separation",
    "QTMCFGIMUINT": "Sets/Gets Motion Trigger Interruption",
    "QTMCFGIMUTC": "Sets/Gets IMU Temperature Compensation",
    "QTMCFGLA": "Sets/Gets Lever Arm",
    "QTMCFGLAM": "Sets/Gets Lever Arm Mode",
    "QTMCFGMSGRATE": "Sets/Gets Message Output Rate",
    "QTMCFGNAVMODE": "Sets/Gets Navigation Mode",
    "QTMCFGNMEADP": "Sets/Gets NMEA Precision",
    "QTMCFGNMEATID": "Sets/Gets NMEA Talker ID",
    "QTMCFGODO": "Sets/Gets Odometer Feature",
    "QTMCFGPPS": "Sets/Gets PPS (Pulse Per Second) Feature",
    "QTMCFGPROT": "Sets/Gets I/O Protocol for Specified Port",
    "QTMCFGRCVRMODE": "Sets/Gets Receiver Working Mode",  # Rover, Base
    "QTMCFGRSID": "Sets/Gets Reference Station ID",
    "QTMCFGRTCM": "Sets/Gets RTCM",
    "QTMCFGRTK": "Sets/Gets RTK Mode",  # Absolute, Relative
    "QTMCFGRTKSRCTYPE": "Sets/Gets RTK Source Type",
    "QTMMCFGRTKSRCTYPE": "Sets/Gets RTK Source Type",  # typo in LG580P firmware?
    "QTMCFGSAT": "Sets/Gets GNSS Satellite Mask",
    "QTMCFGSBAS": "Sets/Gets SBAS",
    "QTMCFGSIGGRP": "Sets/Gets GNSS Signal Group",
    "QTMCFGSIGNAL": "Sets/Gets Antenna1 Signal Mask",
    "QTMCFGSIGNAL2": "Sets/Gets Antenna2 Signal Mask",
    "QTMCFGSTATICHOLD": "Sets/Gets Parking Static Hold",
    "QTMCFGSVIN": "Sets/Gets Survey-In Feature",  # Survey-In or Fixed
    "QTMCFGUART": "Configure UART Interface",
    "QTMCFGVEHMOT": "Sets/Gets Vehicle Motion Detection",
    "QTMCFGWN": "Sets/Gets Reference Start Week No",
    "QTMCOLD": "Cold Start",
    "QTMDEBUGOFF": "Disable Debug Log Output",
    "QTMDEBUGON": "Enable Debug Log Output",
    "QTMDOP": "Outputs Dilution of Precision",
    "QTMDRCAL": "Dead Reckoning Calibration Status",
    "QTMDRCLR": "Clear DR Calibration Data",
    "QTMDRPVA": "DR Postion, Velosity and Attitude",
    "QTMDRSAVE": "Save DR Calibration Data",
    "QTMEOE": "Output End of Epoch Information",
    "QTMEPE": "Output Estimated Position Error",
    "QTMGEOFENCESTATUS": "Outputs Geofence Status",
    "QTMGETUTC": "Get UTC Time Information",
    "QTMGNSSSTART": "Starts GNSS Engine",
    "QTMGNSSSTOP": "Stops GNSS Engine",
    "QTMGPS": "Position Status in GNSS Mode",
    "QTMHOT": "Hot Start",
    "QTMIMU": "IMU Raw Data",
    "QTMIMUTYPE": "IMU Status",
    "QTMINS": "Navigation Results",
    "QTMJAMMINGSTATUS": "Jamming Detection Status",
    "QTMLS": "Outputs Leap Second Forecast Information",
    "QTMNAV": "Output Navigation Information",
    "QTMODO": "Outputs Odometer Information",
    "QTMPL": "Outputs Protection Level Information",
    "QTMPVT": "Outputs PVT (GNSS) Result",  # Position, Velocity, Track
    "QTMQVER": "Queries Version Information",
    "QTMRESETODO": "Reset Odometer Distance",
    "QTMRESTOREPAR": "Restore to Default Values after Restart",
    "QTMSAVEPAR": "Save Configuration to Non-Volatile Memory",
    "QTMSENMSG": "Sensor Information",
    "QTMSN": "Queries Module Serial Number Code",
    "QTMSRR": "System Reset and Reboot",
    "QTMSTD": "Outputs Time, Position, Velocoity and Attitude Deviations",
    "QTMSVINSTATUS": "Outputs Survey-In Status",
    "QTMTAR": "Output Time and Attitude",
    "QTMTXT": "Outputs Short Text Message",  # Longer messages use multiple messages
    "QTMUNIQID": "Query Module Unique ID",
    "QTMVEHATT": "Output Vehicle Attitude",
    "QTMVEHMOT": "Output Vehicle Motion after DR Calibration",
    "QTMVEHMSG": "Output Vehicle Information",
    "QTMVEL": "Output Velocity Information",
    "QTMVER": "Firmware Version",
    "QTMVERNO": "Query Firmware Version",
    "QTMWARM": "Warm Start",
    # ***************************************************************
    # Quectel PSTM Proprietary message types (LG69T)
    # ***************************************************************
    "STMCOLD": "Perform cold start",  # Command
    "STMCPU": "Output CPU usage and speed",  # Output
    "STMDR1": "Report gyroscope and accelerometer details",  # Output
    "STMDR2": "Report calibration status and availability",  # Output
    "STMDRBSD": "Report IMU bias error estimates",  # Output
    "STMDRCAL": "Report IMU and odometer calibration status",  # Output
    "STMDRCONFID": "Report navigation and calibration error estimates",  # Output
    "STMDRDEBUG": "Report DR debug information",  # Output
    "STMDREPE": "Report DR horizontal position error estimates",  # Output
    "STMDRGPS": "Report GNSS information",  # Output
    "STMDRMMFB": "Set DR algorithm input data",  # Command
    "STMDRMMFBKF": "Report MMFB data timing, acceptance, and usage",  # Output
    "STMDRPVA": "Report PVT estimated by DR",  # Output
    "STMDRPVASD": "Report DR PVT error estimates",  # Output
    "STMDRSENMSG": "Output the IMU raw data",  # Output
    "STMDRSINT": "Report sensor integration samples",  # Type:
    "STMDRSTYPE": "Report DR type",  # Output
    "STMDRSVF": "Report IMU vehicle dynamics",  # Output
    "STMDRUPD": "Quectel internal debugging",  # Output
    "STMEPHEM": "Load ephemeris into NVM",  # Command
    "STMHOT": "Perform hot start",  # Command
    "STMIMUSELFTESTCMD": "Execute IMU self-test",  # Command
    "STMINITGPS": "Initialise GPS",  # Command #
    "STMINITGPSERROR": "Initialise GPS Nak",  # Response
    "STMINITGPSOK": "Initialise GPS Ack",  # Response
    "STMINITTIME": "Initialise time",  # Command
    "STMINITTIMEERROR": "Initialise time Nak",  # Response
    "STMINITTIMEOK": "Initialise time Ack",  # Response
    "STMPPSDATA": "Output the PPS data",  # Output
    "STMRESTOREPAR": "Restore the factory setting parameters",  # Command
    "STMSAVEPAR": "Save current configuration data block to NVM",  # Command
    "STMSBAS": "Output SBAS satellite data",  # Output
    "STMSETPAR": "Set parameter",  # Command
    "STMSETPARERROR": "Set parameter Nak",  # Response
    "STMSETPAROK": "Set parameter Ack",  # Response
    "STMSRR": "Execute system reset and reboot",  # Command
    "STMTEMP": "Report temperature",  # Output
    "STMTG": "Output time and satellite information",  # Output
    "STMTS": "Output tracked satellite parameters",  # Output
    "STMWARM": "Perform warm start",  # Command
    # ***************************************************************
    # Sepentrio X5 Proprietary message types
    # ***************************************************************
    "SSNHRP": "Heading, Roll, Pitch",
    "SSNRBD": "Rover Base Direction",
    "SSNRBP": "Rover Base Position",
    "SSNRBV": "Rover Base Velocity",
    "SSNSNC": "NTRIP Client Status",
    "SSNTFM": "Used RTCM Coordinate Transformation Messages",
    # ***************************************************************
    # U-BLOX Proprietary message types
    # ***************************************************************
    "UBX00": "Lat/Long Position Data",
    "UBX03": "Satellite Status",
    "UBX04": "Time of Day and Clock Information",
    "UBX05": "Lat/Long Position Data",
    "UBX06": "Lat/Long Position Data",
    "UBX40": "Set NMEA Message Output Rate",
    "UBX41": "Set Protocols and Baudrate",
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

NMEA_PREFIX_PROP = ("ASHR", "GPPADV", "FEC", "SSN", "TNL", "UBX")
"""
Proprietary NMEA Message Prefixes where `msgId` is part of payload.

For proprietary messages with these prefixes, the `msgId` is defined as
the first element of the payload. The unique payload dictionary key is
therefore a combination of `prefix` + `msgId`.

NB: There are some exceptions which require special handling e.g. `PASHR`.
"""
