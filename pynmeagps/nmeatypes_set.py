"""
NMEA Protocol Set payload definitions

THESE ARE THE PAYLOAD DEFINITIONS FOR _SET_ MESSAGES _TO_ THE RECEIVER
(i.e. Configuration commands)

NB: Attribute names must be unique within each message id

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

:author: semuadmin
"""

from pynmeagps.nmeatypes_core import HX, IN

NMEA_PAYLOADS_SET = {
    # *********************************************
    # STANDARD MESSAGES
    # *********************************************
    # No standard SET messages that I'm aware of
    # *********************************************
    # PROPRIETARY MESSAGES
    # *********************************************
    "PUBX40": {  # set message rates per port
        "msgId": IN,  # 40
        "id": IN,
        "rddc": IN,  # I2C
        "rus1": IN,  # UART1
        "rus2": IN,  # UART2
        "rusb": IN,  # USB
        "rspi": IN,  # SPI
        "reserved": IN,
    },
    "PUBX41": {  # configure port protocols
        "msgId": IN,  # 41
        "portId": IN,
        "inProto": HX,
        "outProto": HX,
        "baudRate": IN,
        "autobauding": IN,
    },
}
