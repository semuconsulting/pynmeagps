"""
NMEA Protocol Proprietary Poll payload definitions

THESE ARE THE PAYLOAD DEFINITIONS FOR PROPRIETARY _POLL_ MESSAGES _TO_
THE RECEIVER (e.g. Message Poll requests).

NB: Attribute names must be unique within each message id.
NB: Avoid reserved names 'msgID', 'talker', 'payload', 'checksum'.

Created on 19 Aug 2024

While the NMEA 0183 © protocol is proprietary, the information here
has been collated from public domain sources.

:author: semuadmin (Steve Smith)
"""

from pynmeagps.nmeatypes_core import IN, QS, ST

NMEA_PAYLOADS_POLL_PROP = {
    # ***************************************************************
    # Quectel LC29H / LC79H Proprietary Poll message types
    # https://www.quectel.com/download/quectel_lc29hlc79h_series_gnss_protocol_specification_v1-5/
    # quectel_lc29hlc79h_series_gnss_protocol_specification_v1-5.pdf
    "AIR051": {},
    "AIR059": {},
    "AIR063": {"type": IN},
    "AIR067": {},
    "AIR071": {},
    "AIR073": {},
    "AIR075": {},
    "AIR081": {},
    "AIR087": {},
    "AIR101": {},
    "AIR105": {},
    "AIR401": {},
    "AIR411": {},
    "AIR421": {},
    "AIR433": {},
    "AIR435": {},
    "AIR491": {},
    "AIR865": {
        "portType": IN,  # 0 = UART
        "portIndex": IN,  # 0 = UART1
    },
    "AIR867": {
        "portType": IN,  # 0 = UART
        "portIndex": IN,  # 0 = UART1
    },
    "AIR6011": {
        "type": IN,
    },
    # ***************************************************************
    # Quectel LG290P Proprietary message types
    # https://quectel.com/content/uploads/2024/09/Quectel_LG290P03_GNSS_Protocol_Specification_V1.0.pdf
    #
    # status attribute must be set to 'R' in all POLL messages
    # ***************************************************************
    "QTMCFGAIC": {"status": QS},
    "QTMCFGANTDELTA": {"status": QS},
    "QTMCFGANTINF": {"status": QS},
    "QTMCFGBLD": {"status": QS},
    "QTMCFGCNST": {"status": QS},
    "QTMCFGDR": {"status": QS},
    "QTMCFGELETHD": {"status": QS},
    "QTMCFGFIXRATE": {"status": QS},
    "QTMCFGGEOFENCE": {"status": QS, "geofenceindex": IN},
    "QTMCFGGEOSEP": {"status": QS},
    "QTMCFGIMUINT": {"status": QS},
    "QTMCFGLA": {"status": QS},
    "QTMCFGLAM": {"status": QS},
    "QTMCFGMSGRATE": {"status": QS, "msgname": ST, "msgver": IN},
    "QTMCFGMSGRATE_NOVER": {"status": QS, "msgname": ST},
    "QTMCFGMSGRATE_INTF": {
        "status": QS,
        "porttype": IN,
        "portid": IN,
        "msgname": ST,
        "msgver": IN,
    },
    "QTMCFGMSGRATE_INTFNOVER": {
        "status": QS,
        "porttype": IN,
        "portid": IN,
        "msgname": ST,
    },
    "QTMCFGNAVMODE": {"status": QS},
    "QTMCFGNMEADP": {"status": QS},
    "QTMCFGNMEATID": {"status": QS},
    "QTMCFGODO": {"status": QS},
    "QTMCFGPPS": {"status": QS, "ppsindex": IN},
    "QTMCFGPROT": {"status": QS, "porttype": IN, "portid": IN},
    "QTMCFGRCVRMODE": {"status": QS},
    "QTMCFGRSID": {"status": QS},
    "QTMCFGRTCM": {"status": QS},
    "QTMCFGRTK": {"status": QS},
    "QTMCFGRTKSRCTYPE": {"status": QS},
    "QTMCFGSAT": {"status": QS, "systemid": IN, "signalid": ST},
    "QTMCFGSBAS": {"status": QS},
    "QTMCFGSIGGRP": {"status": QS},
    "QTMCFGSIGNAL": {"status": QS},
    "QTMCFGSIGNAL2": {"status": QS},
    "QTMCFGSTATICHOLD": {"status": QS},
    "QTMCFGSVIN": {"status": QS},
    "QTMCFGUART_CURR": {"status": QS},
    "QTMCFGUART": {"status": QS, "portid": IN},
    "QTMCFGVEHMOT": {"status": QS},
    "QTMCFGWN": {"status": QS},
    "QTMGETUTC": {},
    "QTMQVER": {"msgver": IN},
    "QTMSN": {},
    "QTMUNIQID": {},
    "QTMVEHATT": {},
    "QTMVERNO": {},
}
