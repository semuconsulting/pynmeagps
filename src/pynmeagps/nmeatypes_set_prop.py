"""
NMEA Protocol Proprietary Set payload definitions

THESE ARE THE PAYLOAD DEFINITIONS FOR PROPRIETARY _SET_ MESSAGES _TO_
THE RECEIVER (e.g. Configuration commands).

NB: Attribute names must be unique within each message id.
NB: Avoid reserved names 'msgID', 'talker', 'payload', 'checksum'.

NB: Repeating groups must be defined as a tuple thus
    'group': ('numr', {dict})
    where
    - 'numr' is either:
       a) an integer representing a fixed number of repeats e.g 32
       b) a string representing the name of a preceding attribute
          containing the number of repeats e.g. 'numCh'
       c) 'None' for an indeterminate repeating group
          (only one such group is permitted per message type)
    - {dict} is the nested dictionary containing the repeating
      attributes

Created on 19 Aug 2024

While the NMEA 0183 © protocol is proprietary, the information here
has been collated from public domain sources.

:author: semuadmin (Steve Smith)
"""

from pynmeagps.nmeatypes_core import CH, DE, DT, HX, IN, LA, LAD, LN, LND, QS, ST, TM
from pynmeagps.nmeatypes_get_prop import NMEA_PAYLOADS_GET_PROP

NMEA_PAYLOADS_SET_PROP = {
    # ***************************************************************
    # Quectel LC29H / LC79H Proprietary SET message types
    # https://www.quectel.com/download/quectel_lc29hlc79h_series_gnss_protocol_specification_v1-5/
    # quectel_lc29hlc79h_series_gnss_protocol_specification_v1-5.pdf
    # ***************************************************************
    "AIR002": {},
    "AIR003": {},
    "AIR004": {},
    "AIR005": {},
    "AIR006": {},
    "AIR007": {},
    "AIR050": {
        "time": IN,
    },
    "AIR058": {
        "minsnr": IN,
    },
    "AIR062": {
        "type": IN,
        "rate": IN,
    },
    "AIR066": {
        "gpsEnabled": IN,
        "glonassEnabled": IN,
        "galileoEnabled": IN,
        "bdsEnabled": IN,
        "qzssEnabled": IN,
        "navicEnabled": IN,
    },
    "AIR070": {
        "speedThreshold": IN,
    },
    "AIR072": {
        "degree": IN,
    },
    "AIR074": {
        "enabled": IN,
    },
    "AIR080": {
        "navMode": IN,
    },
    "AIR086": {
        "status": IN,
    },
    "AIR100": {
        "nmeaMode": IN,
        "reserved": IN,
    },
    "AIR104": {
        "dualBandEnabled": IN,
    },
    "AIR382": {
        "enabled": IN,
    },
    "AIR391": {
        "cmdType": IN,
    },
    "AIR400": {
        "mode": IN,
    },
    "AIR410": {
        "enabled": IN,
    },
    "AIR420": {
        "enabled": IN,
    },
    "AIR432": {
        "mode": IN,
    },
    "AIR434": {
        "enabled": IN,
    },
    "AIR436": {
        "enabled": IN,
    },
    "AIR437": {},
    "AIR490": {
        "enabled": IN,
    },
    "AIR511": {},
    "AIR512": {},
    "AIR513": {},
    "AIR650": {
        "second": IN,
    },
    "AIR752": {
        "ppsType": IN,
    },
    "AIR864": {
        "portType": IN,  # 0 = UART
        "portIndex": IN,  # 0 = UART1
        "baudrate": IN,
    },
    "AIR866": {
        "portType": IN,  # 0 = UART
        "portIndex": IN,  # 0 = UART1
        "flowControl": IN,
    },
    "AIR6010": {
        "type": IN,
        "rate": IN,
    },
    # *********************************************
    # GARMIN PROPRIETARY MESSAGES
    # *********************************************
    "GRMI": {  # sensor initialisation information
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "date": DT,
        "time": TM,
        "rcvr_cmd": CH,
    },
    "GRMC": {  # sensor configuration information
        "fix": CH,
        "alt": DE,
        "dtm": ST,
        "smAxis": DE,
        "iffac": DE,
        "xecc": DE,
        "yecc": DE,
        "zecc": DE,
        "diff": CH,
        "baudRate": IN,
        "vfilt": IN,
        "reserved1": ST,
        "reserved2": ST,
        "drtime": IN,
    },
    "GRMC1": {  # additional sensor configuration information
        "nmeatim": IN,
        "bphase": IN,
        "autopos": IN,
        "dgpsfr": DE,
        "dgpsbr": IN,
        "dgpssc": IN,
        "nmeaver": IN,
        "dgpsmod": CH,
        "pwrsave": CH,
        "attran": IN,
        "autopwr": IN,
        "extpwr": IN,
    },
    "GRMO": {  # output sentence enable
        "msgId": ST,
        "tgtmode": IN,
    },
    "GRMW": {  # additional waypoint information
        "wptId": ST,
        "alt": DE,
        "symnum": HX,
        "comment": ST,
    },
    # ***************************************************************
    # Locosys Proprietary Messages SET
    # https://www.locosystech.com/Templates/att/LS2303x-UDG_datasheet_v0.6.pdf?lng=en
    # ***************************************************************
    # Proprietary Locosys command sets not yet implemented, e.g.
    # Perform a Cold start $PMTK103*30
    # Perform a Warm start $PMTK102*31
    # Perform a Hot start $PMTK101*32
    # Perform a Full Cold start $PMTK104*37
    # Disable GLL message $PMTK314,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0*29
    # Disable GSV message $PMTK314,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0*29
    # Disable GLL & GSV message $PMTK314,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0*28
    # Factory default output message $PMTK314,-1*04
    # Navigate with GPS+GALILEO $PMTK353,1,0,1,0,0*2B
    # Navigate with GPS+GLONASS+GALILEO $PMTK353,1,1,1,0,0*2A
    # Navigate with GPS+BEIDOU $PMTK353,1,0,0,0,1*2B
    # Entering Standby Mode1 $PMTK161,0*28
    "INVCRES": {
        "value": IN,  # 0 = clear data
    },
    "INVCSTR": {
        "value": IN,  # 14 = start session
    },
    "INVMSLOPE": {
        "status": IN,  # 0 = disable, 1 =  enable
    },
    "LSC": {
        "msgType": ST,  # e.g. "SLOPE", "MEMS", "ATTIT", "VER"
        "value": IN,  # e.g. 0 (not present if msgType == "VER")
    },
    # ***************************************************************
    # Quectel LG290P Proprietary message types
    # https://quectel.com/content/uploads/2024/09/Quectel_LG290P03_GNSS_Protocol_Specification_V1.0.pdf
    # ***************************************************************
    "QTMBKP": {
        "second": IN,
    },
    "QTMCFGAIC": NMEA_PAYLOADS_GET_PROP["QTMCFGAIC"],
    "QTMCFGANTDELTA": NMEA_PAYLOADS_GET_PROP["QTMCFGANTDELTA"],
    "QTMCFGANTINF": NMEA_PAYLOADS_GET_PROP["QTMCFGANTINF"],
    "QTMCFGBLD": NMEA_PAYLOADS_GET_PROP["QTMCFGBLD"],
    "QTMCFGCNST": NMEA_PAYLOADS_GET_PROP["QTMCFGCNST"],
    "QTMCFGDR": NMEA_PAYLOADS_GET_PROP["QTMCFGDR"],
    "QTMCFGDRHOT": NMEA_PAYLOADS_GET_PROP["QTMCFGDRHOT"],
    "QTMCFGDRRTD": NMEA_PAYLOADS_GET_PROP["QTMCFGDRRTD"],
    "QTMCFGEINSMSG": NMEA_PAYLOADS_GET_PROP["QTMCFGEINSMSG"],
    "QTMCFGELETHD": NMEA_PAYLOADS_GET_PROP["QTMCFGELETHD"],
    "QTMCFGFIXRATE": NMEA_PAYLOADS_GET_PROP["QTMCFGFIXRATE"],
    "QTMCFGGEOFENCE_DIS": NMEA_PAYLOADS_GET_PROP["QTMCFGGEOFENCE_DIS"],
    "QTMCFGGEOFENCE_POLY": NMEA_PAYLOADS_GET_PROP["QTMCFGGEOFENCE_POLY"],
    "QTMCFGGEOFENCE": NMEA_PAYLOADS_GET_PROP["QTMCFGGEOFENCE"],
    "QTMCFGGEOSEP": NMEA_PAYLOADS_GET_PROP["QTMCFGGEOSEP"],
    "QTMCFGIMUINT": NMEA_PAYLOADS_GET_PROP["QTMCFGIMUINT"],
    "QTMCFGIMUTC": NMEA_PAYLOADS_GET_PROP["QTMCFGIMUTC"],
    "QTMCFGLA": NMEA_PAYLOADS_GET_PROP["QTMCFGLA"],
    "QTMCFGLAM": NMEA_PAYLOADS_GET_PROP["QTMCFGLAM"],
    "QTMCFGMSGRATE": NMEA_PAYLOADS_GET_PROP["QTMCFGMSGRATE"],
    "QTMCFGMSGRATE_NOVER": NMEA_PAYLOADS_GET_PROP["QTMCFGMSGRATE_NOVER"],
    "QTMCFGMSGRATE_INTF": NMEA_PAYLOADS_GET_PROP["QTMCFGMSGRATE_INTF"],
    "QTMCFGMSGRATE_INTFNOVER": NMEA_PAYLOADS_GET_PROP["QTMCFGMSGRATE_INTFNOVER"],
    "QTMCFGNAVMODE": NMEA_PAYLOADS_GET_PROP["QTMCFGNAVMODE"],
    "QTMCFGNMEADP": NMEA_PAYLOADS_GET_PROP["QTMCFGNMEADP"],
    "QTMCFGNMEATID": NMEA_PAYLOADS_GET_PROP["QTMCFGNMEATID"],
    "QTMCFGODO": NMEA_PAYLOADS_GET_PROP["QTMCFGODO"],
    "QTMCFGPPS": NMEA_PAYLOADS_GET_PROP["QTMCFGPPS"],
    "QTMCFGSBAS": NMEA_PAYLOADS_GET_PROP["QTMCFGSBAS"],
    "QTMCFGSIGGRP": NMEA_PAYLOADS_GET_PROP["QTMCFGSIGGRP"],
    "QTMCFGPPS_DIS": {
        "status": QS,
        "ppsindex": IN,
        "enable": IN,  # should be 0
    },
    "QTMCFGPROT": NMEA_PAYLOADS_GET_PROP["QTMCFGPROT"],
    "QTMCFGRCVRMODE": NMEA_PAYLOADS_GET_PROP["QTMCFGRCVRMODE"],
    "QTMCFGRSID": NMEA_PAYLOADS_GET_PROP["QTMCFGRSID"],
    "QTMCFGRTCM": NMEA_PAYLOADS_GET_PROP["QTMCFGRTCM"],
    "QTMCFGRTK": NMEA_PAYLOADS_GET_PROP["QTMCFGRTK"],
    "QTMCFGRTKSRCTYPE": NMEA_PAYLOADS_GET_PROP["QTMCFGRTKSRCTYPE"],
    "QTMCFGSAT_LOW": NMEA_PAYLOADS_GET_PROP["QTMCFGSAT_LOW"],
    "QTMCFGSAT": NMEA_PAYLOADS_GET_PROP["QTMCFGSAT"],
    "QTMCFGSIGNAL": NMEA_PAYLOADS_GET_PROP["QTMCFGSIGNAL"],
    "QTMCFGSIGNAL2": NMEA_PAYLOADS_GET_PROP["QTMCFGSIGNAL2"],
    "QTMCFGSTATICHOLD": NMEA_PAYLOADS_GET_PROP["QTMCFGSTATICHOLD"],
    "QTMCFGSVIN": NMEA_PAYLOADS_GET_PROP["QTMCFGSVIN"],
    "QTMCFGWN": NMEA_PAYLOADS_GET_PROP["QTMCFGWN"],
    # sets all parms for specified interface:
    "QTMCFGUART": NMEA_PAYLOADS_GET_PROP["QTMCFGUART"],
    "QTMCFGVEHMOT": NMEA_PAYLOADS_GET_PROP["QTMCFGVEHMOT"],
    # sets baud rate for specified interface
    "QTMCFGUART_BAUD": {
        "status": QS,
        "portid": IN,
        "baudrate": IN,
    },
    # sets all parms for current interface:
    "QTMCFGUART_CURR": {
        "status": QS,
        "baudrate": IN,
        "databit": IN,
        "parity": IN,
        "stopbit": IN,
        "flowctrl": IN,
    },
    # sets baud rate for current interface:
    "QTMCFGUART_CURRBAUD": {
        "status": QS,
        "baudrate": IN,
    },
    "QTMCOLD": {},
    "QTMDEBUGOFF": {},
    "QTMDEBUGON": {},
    "QTMDRCLR": {},
    "QTMDRSAVE": {},
    "QTMGNSSSTART": {},
    "QTMGNSSSTOP": {},
    "QTMHOT": {},
    "QTMRESETODO": {},
    "QTMRESTOREPAR": {},
    "QTMSAVEPAR": {},
    "QTMSRR": {},
    "QTMWARM": {},
    # ***************************************************************
    # Quectel LG69T PSTM Proprietary message types
    # https://quectel.com/content/uploads/2024/09/quectel_lg69taaadafaiajar_gnss_protocol_specification_v1-5.pdf
    # ***************************************************************
    "STMCOLD": {},
    "STMWARM": {},
    "STMEPHEM": {
        "satID": IN,
        "ephdatalen": IN,
        "ephdata": HX,
    },
    "STMHOT": {},
    "STMSRR": {},
    "STMSAVEPAR": {},
    "STMRESTOREPAR": {},
    "STMSETPAR": {
        "parm1": IN,
        "parm2": IN,
        "parm3": IN,
        "parm4": IN,
        "parm5": ST,
    },
    "STMIMUSELFTESTCMD": {"imucat": IN},
    "STMINITGPS": {
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "alt": DE,
        "day": IN,
        "month": IN,
        "year": IN,
        "hour": IN,
        "minute": IN,
        "second": IN,
    },
    "STMINITTIME": {
        "day": IN,
        "month": IN,
        "year": IN,
        "hour": IN,
        "minute": IN,
        "second": IN,
    },
    "STMDRMMFB": {
        "timestamp": DE,
        "latval": IN,
        "lonval": IN,
        "heightval": IN,
        "headingval": IN,
        "lat": DE,
        "lon": DE,
        "height": DE,
        "heading": DE,
        "laterr": DE,
        "lonerr": DE,
        "heighterr": DE,
        "headingerr": DE,
    },
    # *********************************************
    # U-BLOX PROPRIETARY MESSAGES
    # *********************************************
    "UBX40": {  # set message rates per port
        "msgId": ST,  # '40'
        "id": ST,  # e.g. GLL
        "rddc": IN,  # I2C
        "rus1": IN,  # UART1
        "rus2": IN,  # UART2
        "rusb": IN,  # USB
        "rspi": IN,  # SPI
        "reserved": IN,
    },
    "UBX41": {  # configure port protocols
        "msgId": ST,  # '41'
        "portId": IN,
        "inProto": HX,
        "outProto": HX,
        "baudRate": IN,
        "autobauding": IN,
    },
}
