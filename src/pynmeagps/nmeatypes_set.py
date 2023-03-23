"""
NMEA Protocol Set payload definitions

THESE ARE THE PAYLOAD DEFINITIONS FOR _SET_ MESSAGES _TO_ THE RECEIVER
(e.g. Configuration commands).

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

Created on 4 Mar Sep 2021

While the NMEA 0183 © protocol is proprietary, the information here
has been collated from public domain sources.

:author: semuadmin
"""

from pynmeagps.nmeatypes_core import (
    CH,
    DE,
    DT,
    HX,
    IN,
    LA,
    LN,
    ST,
    TM,
)

NMEA_PAYLOADS_SET = {
    # *********************************************
    # STANDARD MESSAGES
    # *********************************************
    # No standard SET messages that I'm aware of
    # *********************************************
    # GARMIN PROPRIETARY MESSAGES
    # *********************************************
    "GRMI": {  # sensor initialisation information
        "lat": LA,
        "NS": CH,
        "lon": LN,
        "EW": CH,
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
