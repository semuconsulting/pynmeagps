"""
NMEA Protocol Poll payload definitions

THESE ARE THE PAYLOAD DEFINITIONS FOR _POLL_ MESSAGES _TO_ THE RECEIVER
(i.e. Message Poll requests)

NB: Attribute names must be unique within each message id

Created on 4 Mar Sep 2021

:author: semuadmin
"""

from pynmeagps.nmeatypes_core import (
    IN,
    ST,
)

NMEA_PAYLOADS_POLL = {
    # *********************************************
    # STANDARD MESSAGES
    # *********************************************
    "GAQ": {  # Galileo
        "msgId": ST,
    },
    "GBQ": {  # BeiDou
        "msgId": ST,
    },
    "GLQ": {  # GLONASS
        "msgId": ST,
    },
    "GNQ": {  # Any GNSS
        "msgId": ST,
    },
    "GPQ": {  # GPS, SBAS
        "msgId": ST,
    },
    "GQQ": {  # QZSS
        "msgId": ST,
    },
    # *********************************************
    # PROPRIETARY MESSAGES
    # *********************************************
    "PUBX00": {
        "msgId": IN,  # 00
    },
    "PUBX03": {
        "msgId": IN,  # 03
    },
    "PUBX04": {
        "msgId": IN,  # 04
    },
}
