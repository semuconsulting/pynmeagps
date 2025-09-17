"""
NMEA Protocol Poll payload definitions

THESE ARE THE PAYLOAD DEFINITIONS FOR _POLL_ MESSAGES _TO_ THE RECEIVER
(e.g. Message Poll requests).

NB: Attribute names must be unique within each message id.
NB: Avoid reserved names 'msgID', 'talker', 'payload', 'checksum'.

Created on 4 Mar Sep 2021

While the NMEA 0183 © protocol is proprietary, the information here
has been collated from public domain sources.

:author: semuadmin (Steve Smith)
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
    # u-blox
    "UBX00": {
        "msgId": ST,  # '00'
    },
    "UBX03": {
        "msgId": ST,  # '03'
    },
    "UBX04": {
        "msgId": ST,  # '04'
    },
    "UBX05": {
        "msgId": ST,  # '05'
    },
    "UBX06": {
        "msgId": ST,  # '06'
    },
    # Garmin
    "GRMB": {},
    "GRMC": {},
    "GRMC1": {},
    "GRME": {},
    "GRMF": {},
    "GRMH": {},
    "GRMI": {},
    "GRMM": {},
    "GRMO": {},
    "GRMT": {},
    "GRMV": {},
    "GRMW": {},
    "GRMZ": {},
    # Trimble
    "ASHRALR": {
        "msgId": ST,  # 'ALR'
    },
    "ASHRARA": {
        "msgId": ST,  # 'ARA'
    },
    "ASHRARR": {
        "msgId": ST,  # 'ARR'
    },
    "ASHRATT": {
        "msgId": ST,  # 'ATT'
    },
    "ASHRBTS": {
        "msgId": ST,  # 'BTS'
    },
    "ASHRCAP": {
        "msgId": ST,  # 'CAP'
    },
    "ASHRCPA": {
        "msgId": ST,  # 'CPA'
    },
    "ASHRCPO": {
        "msgId": ST,  # 'CPO'
    },
    "ASHRDDM": {
        "msgId": ST,  # 'DDM'
    },
    "ASHRDDS": {
        "msgId": ST,  # 'DDS'
    },
    "ASHRHPR": {
        "msgId": ST,  # 'HPR'
    },
    "ASHRHR": {
        "msgId": ST,  # 'HR'
    },
    "ASHRLTN": {
        "msgId": ST,  # 'LTN'
    },
    "ASHRMDM": {
        "msgId": ST,  # 'MDM'
    },
    "ASHRPOS": {
        "msgId": ST,  # 'POS'
    },
    "ASHRPBN": {
        "msgId": ST,  # 'PBN'
    },
    "ASHRPTT": {
        "msgId": ST,  # 'PTT'
    },
    "ASHRPWR": {
        "msgId": ST,  # 'PWR'
    },
    "ASHRRCS": {
        "msgId": ST,  # 'RCS'
    },
    "ASHRSBD": {
        "msgId": ST,  # 'SBD'
    },
    "ASHRSGA": {
        "msgId": ST,  # 'SGA'
    },
    "ASHRSGL": {
        "msgId": ST,  # 'SGL'
    },
    "ASHRSGO": {
        "msgId": ST,  # 'SGO'
    },
    "ASHRSGP": {
        "msgId": ST,  # 'SGP'
    },
    "ASHRSIR": {
        "msgId": ST,  # 'SIR'
    },
    "ASHRSLB": {
        "msgId": ST,  # 'SLB'
    },
    "ASHRSQZ": {
        "msgId": ST,  # 'SQZ'
    },
    "ASHRSSB": {
        "msgId": ST,  # 'SSB'
    },
    "ASHRTEM": {
        "msgId": ST,  # 'TEM'
    },
    "ASHRTHS": {
        "msgId": ST,  # 'THS'
    },
    "ASHRTTT": {
        "msgId": ST,  # 'TTT'
    },
    "ASHRVCR": {
        "msgId": ST,  # 'VCR'
    },
    "ASHRVCT": {
        "msgId": ST,  # 'VCT'
    },
    "ASHRVEL": {
        "msgId": ST,  # 'VEL'
    },
    "FUGDP": {},
    "GPPADV110": {
        "msgId": ST,  # '110'
    },
    "GPPADV120": {
        "msgId": ST,  # '120'
    },
    "TNLAVR": {
        "msgId": ST,  # 'AVR'
    },
    "TNLBPQ": {
        "msgId": ST,  # 'BPQ'
    },
    "TNLDG": {
        "msgId": ST,  # 'DG'
    },
    "TNLEVT": {
        "msgId": ST,  # 'EVT'
    },
    "TNLGGK": {
        "msgId": ST,  # 'GGK'
    },
    "TNLGGKx": {
        "msgId": ST,  # 'GGKx'
    },
    "TNLPJK": {
        "msgId": ST,  # 'PJK'
    },
    "TNLPJT": {
        "msgId": ST,  # 'PJT'
    },
    "TNLREX": {
        "msgId": ST,  # 'REX'
    },
    "TNLVGK": {
        "msgId": ST,  # 'VGK'
    },
    "TNLVHD": {
        "msgId": ST,  # 'VHD'
    },
}
