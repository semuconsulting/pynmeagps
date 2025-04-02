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

:author: semuadmin
"""

from pynmeagps.nmeatypes_core import CH, DE, DT, HX, IN, LA, LAD, LN, LND, QS, ST, TM
from pynmeagps.nmeatypes_get_prop import NMEA_PAYLOADS_GET_PROP

NMEA_PAYLOADS_SET_PROP = {
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
    "LSC": {
        "msgType": ST,  # e.g. "SLOPE", "MEMS", "ATTIT", "VER"
        "value": IN,  # e.g. 0 (not present if msgType == "VER")
    },
    "INVCRES": {
        "value": IN,  # 0 = clear data
    },
    "INVCSTR": {
        "value": IN,  # 14 = start session
    },
    "INVMSLOPE": {
        "status": IN,  # 0 = disable, 1 =  enable
    },
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
    # ***************************************************************
    # Quectel LG290P Proprietary message types
    # https://quectel.com/content/uploads/2024/09/Quectel_LG290P03_GNSS_Protocol_Specification_V1.0.pdf
    # ***************************************************************
    "QTMCFGCNST": NMEA_PAYLOADS_GET_PROP["QTMCFGCNST"],
    "QTMCFGFIXRATE": NMEA_PAYLOADS_GET_PROP["QTMCFGFIXRATE"],
    "QTMCFGGEOFENCE": NMEA_PAYLOADS_GET_PROP["QTMCFGGEOFENCE"],
    "QTMCFGGEOFENCE_POLY": NMEA_PAYLOADS_GET_PROP["QTMCFGGEOFENCE_POLY"],
    "QTMCFGGEOFENCE_DIS": NMEA_PAYLOADS_GET_PROP["QTMCFGGEOFENCE_DIS"],
    "QTMCFGMSGRATE_NOVER": NMEA_PAYLOADS_GET_PROP["QTMCFGMSGRATE_NOVER"],
    "QTMCFGMSGRATE": NMEA_PAYLOADS_GET_PROP["QTMCFGMSGRATE"],
    "QTMCFGNMEADP": NMEA_PAYLOADS_GET_PROP["QTMCFGNMEADP"],
    "QTMCFGODO": NMEA_PAYLOADS_GET_PROP["QTMCFGODO"],
    "QTMCFGPPS": NMEA_PAYLOADS_GET_PROP["QTMCFGPPS"],
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
    "QTMCFGSAT": NMEA_PAYLOADS_GET_PROP["QTMCFGSAT"],
    "QTMCFGSAT_LOW": NMEA_PAYLOADS_GET_PROP["QTMCFGSAT_LOW"],
    "QTMCFGSIGNAL": NMEA_PAYLOADS_GET_PROP["QTMCFGSIGNAL"],
    "QTMCFGSVIN": NMEA_PAYLOADS_GET_PROP["QTMCFGSVIN"],
    # sets all parms for specified interface:
    "QTMCFGUART": NMEA_PAYLOADS_GET_PROP["QTMCFGUART"],
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
    "QTMGNSSSTART": {},
    "QTMGNSSSTOP": {},
    "QTMHOT": {},
    "QTMRESETODO": {},
    "QTMRESTOREPAR": {},
    "QTMSAVEPAR": {},
    "QTMSRR": {},
    "QTMUNIQID": {},
    "QTMVERNO": {},
    "QTMWARM": {},
    # *********************************************
    # U-BLOX PROPRIETARY MESSAGES
    # *********************************************
    "UBX40": {  # set message rates per port
        "msgId": ST,  # '40'
        "id": IN,
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
