"""
NMEA Protocol Poll payload definitions

THESE ARE THE PAYLOAD DEFINITIONS FOR _POLL_ MESSAGES _TO_ THE RECEIVER
(e.g. Message Poll requests).

NB: Attribute names must be unique within each message id.
NB: Avoid reserved names 'msgID', 'talker', 'payload', 'checksum'.

Created on 4 Mar Sep 2021

While the NMEA 0183 © protocol is proprietary, the information here
has been collated from public domain sources.

:author: semuadmin
"""

from pynmeagps.nmeatypes_core import ST

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
    "UBX00": {
        "msgId": ST,  # '00'
    },
    "UBX03": {
        "msgId": ST,  # '03'
    },
    "UBX04": {
        "msgId": ST,  # '04'
    },
}
