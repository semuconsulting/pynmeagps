"""
NMEA Protocol Proprietary Poll payload definitions

THESE ARE THE PAYLOAD DEFINITIONS FOR PROPRIETARY _POLL_ MESSAGES _TO_
THE RECEIVER (e.g. Message Poll requests).

NB: Attribute names must be unique within each message id.
NB: Avoid reserved names 'msgID', 'talker', 'payload', 'checksum'.

Created on 19 Aug 2024

While the NMEA 0183 © protocol is proprietary, the information here
has been collated from public domain sources.

:author: semuadmin
"""

from pynmeagps.nmeatypes_core import IN, QS, ST

NMEA_PAYLOADS_POLL_PROP = {
    # ***************************************************************
    # Quectel LG290P Proprietary message types
    # https://quectel.com/content/uploads/2024/09/Quectel_LG290P03_GNSS_Protocol_Specification_V1.0.pdf
    #
    # status attribute must be set to 'R' in all POLL messages
    # ***************************************************************
    "QTMCFGCNST": {"status": QS},
    "QTMCFGFIXRATE": {"status": QS},
    "QTMCFGGEOFENCE": {"status": QS, "geofenceindex": IN},
    "QTMCFGMSGRATE_NOVER": {"status": QS, "msgname": ST},
    "QTMCFGMSGRATE": {"status": QS, "msgname": ST, "msgver": IN},
    "QTMCFGNMEADP": {"status": QS},
    "QTMCFGODO": {"status": QS},
    "QTMCFGPPS": {"status": QS, "ppsindex": IN},
    "QTMCFGPROT": {"status": QS, "porttype": IN, "portid": IN},
    "QTMCFGRCVRMODE": {"status": QS},
    "QTMCFGRSID": {"status": QS},
    "QTMCFGRTCM": {"status": QS},
    "QTMCFGRTK": {"status": QS},
    "QTMCFGSAT": {"status": QS, "systemid": IN, "signalid": ST},
    "QTMCFGSIGNAL": {"status": QS},
    "QTMCFGSVIN": {"status": QS},
    "QTMCFGUART": {"status": QS, "portid": IN},
    "QTMCFGUART_CURR": {"status": QS},
    "QTMUNIQID": {},
    "QTMVERNO": {},
}
