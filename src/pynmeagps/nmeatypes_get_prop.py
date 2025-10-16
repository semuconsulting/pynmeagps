"""
NMEA Protocol Proprietary Output (GET) payload definitions

THESE ARE THE PAYLOAD DEFINITIONS FOR PROPRIETARY _GET_ MESSAGES _FROM_
THE RECEIVER (e.g. Periodic Navigation Data; Poll Responses; Info messages).

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

:author: semuadmin (Steve Smith)
"""

# pylint: disable=too-many-lines, duplicate-code

from pynmeagps.nmeatypes_core import (
    CH,
    DE,
    DM,
    DT,
    HX,
    IN,
    LA,
    LAD,
    LN,
    LND,
    QS,
    ST,
    TM,
)

NMEA_PAYLOADS_GET_PROP = {
    # *********************************************
    # JVC KENWOOD PROPRIETARY MESSAGES
    # *********************************************
    "KLDS": {
        "time": TM,
        "status": CH,
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "sog": DE,
        "cog": DE,
        "dat": DT,
        "declination": DE,
        "dec_dir": CH,
        "fleet": DE,
        "senderid": ST,
        "senderstatus": DE,
        "reserved": DE,
    },
    "KLSH": {
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "time": TM,
        "status": CH,
        "fleetId": ST,
        "deviceId": ST,
    },
    "KNDS": {
        "time": TM,
        "status": CH,
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "sog": DE,
        "cog": DE,
        "date": DT,
        "declination": DE,
        "dec_dir": CH,
        "senderid": ST,
        "senderstatus": DE,
        "reserved": DE,
    },
    "KNSH": {
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "time": TM,
        "status": CH,
        "senderid": ST,
    },
    "KWDWPL": {
        "time": TM,
        "status": CH,
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "sog": DE,
        "cog": DE,
        "date": DT,
        "alt": DE,
        "wpt": ST,
        "ts": ST,
    },
    # *********************************************
    # MAGELLAN PROPRIETARY MESSAGES
    # *********************************************
    "MGNWPL": {
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "alt": DE,
        "alt_unit": CH,
        "wpt": ST,
        "comment": ST,
        "icon": ST,
        "type": ST,
    },
    # *********************************************
    # GARMIN PROPRIETARY MESSAGES
    # *********************************************
    "GRME": {  # estimated error information
        "HPE": DE,
        "HPEUnit": CH,
        "VPE": DE,
        "VPEUnit": CH,
        "EPE": DE,
        "EPEUnit": CH,
    },
    "GRMF": {  # GPS fix data sentence
        "week": IN,
        "secs": IN,
        "date": DT,
        "time": TM,
        "leapsec": IN,
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "mode": CH,
        "fix": IN,
        "spd": DE,
        "course": IN,
        "PDOP": DE,
        "TDOP": DE,
    },
    "GRMH": {  # aviation height and VNAV data
        "status": CH,
        "vspd": DE,
        "verr": DE,
        "spdtgt": DE,
        "spdwpt": DE,
        "height": DE,
        "trk": DE,
        "course": DE,
    },
    "GRMM": {  # map datum
        "dtm": ST,
    },
    "GRMT": {  # sensor status information
        "ver": ST,
        "ROMtest": CH,
        "rcvrtest": CH,
        "stortest": CH,
        "rtctest": CH,
        "osctest": CH,
        "datatest": CH,
        "temp": DE,
        "cfgdata": CH,
    },
    "GRMV": {  # 3D velocity information
        "velE": DE,
        "velN": DE,
        "velZ": DE,
    },
    "GRMZ": {  # altitude
        "alt": DE,
        "altUnit": CH,
        "fix": IN,
    },
    "GRMB": {  # DGPS Beacon information
        "freq": DE,
        "bps": IN,
        "snr": IN,
        "quality": IN,
        "dist": DE,
        "status": IN,
        "fixsrc": CH,
        "mode": CH,
    },
    # *********************************************
    # U-BLOX PROPRIETARY MESSAGES
    # *********************************************
    "UBX00": {
        "msgId": ST,  # '00'
        "time": TM,
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "altRef": DE,
        "navStat": ST,
        "hAcc": DE,
        "vAcc": DE,
        "SOG": DE,
        "COG": DE,
        "vVel": DE,
        "diffAge": DE,
        "HDOP": DE,
        "VDOP": DE,
        "TDOP": DE,
        "numSVs": IN,
        "reserved": IN,
        "DR": IN,
    },
    "UBX03": {
        "msgId": ST,  # '03'
        "numSv": IN,
        "groupSV": (
            "numSv",
            {  # repeating group * numSv
                "svid": IN,
                "status": CH,
                "azi": DE,
                "ele": DE,
                "cno": IN,
                "lck": IN,
            },
        ),
    },
    "UBX04": {
        "msgId": ST,  # '04'
        "time": TM,
        "date": DT,
        "utcTow": ST,
        "utcWk": ST,
        "leapSec": ST,
        "clkBias": DE,
        "clkDrift": DE,
        "tpGran": IN,
    },
    "UBX05": {  # deprecated, for backwards compat only
        "msgId": ST,  # '05'
        "pulses": IN,
        "period": IN,
        "gyroMean": IN,
        "temperature": DE,
        "direction": CH,
        "pulseScaleCS": IN,
        "gyroScaleCS": IN,
        "gyroBiasCS": IN,
        "pulseScale": DE,
        "gyroBias": DE,
        "gyroScale": DE,
        "pulseScaleAcc": IN,
        "gyroBiasAcc": IN,
        "gyroScaleAcc": IN,
        "measUsed": HX,
    },
    # ***************************************************************
    # Trimble Proprietary message types
    # https://receiverhelp.trimble.com/alloy-gnss/en-us/NMEA-0183messages_MessageOverview.html
    # ***************************************************************
    "ASHR": {
        "utctime": TM,
        "trueHdg": DE,
        "trueHdgInd": CH,  # "T"
        "roll": DE,
        "pitch": DE,
        "reserved": ST,
        "rollAcc": DE,
        "pitchAcc": DE,
        "hdgAcc": DE,
        "gnssQual": IN,
        "imuAlign": IN,
    },
    "ASHRALR": {
        "msgId": ST,  # "ALR"
        "alarmCode": IN,
        "alarmSubcode": IN,
        "streamId": CH,
        "alarmCat": ST,
        "alarmLevel": IN,
        "desc": ST,
    },
    "ASHRARA": {
        "msgId": ST,  # "ARA"
        "valid": CH,  # = "0" when valid
        "utctime": TM,
        "hdgSpeed": DE,
        "pitchSpeed": DE,
        "rollSpeed": DE,
        "hdgAcc": DE,
        "pitchAcc": DE,
        "rollAcc": DE,
        "reserved": ST,
    },
    "ASHRARR": {
        "msgId": ST,  # "ARR"
        "vectNum": IN,
        "vectMode": IN,
        "sip": IN,
        "utctime": TM,
        "antEcefX": DE,
        "antEcefY": DE,
        "antEcefZ": DE,
        "coord1std": DE,
        "coord2std": DE,
        "coord3std": DE,
        "coord12corr": DE,
        "coord13corr": DE,
        "coord23corr": DE,
        "refId": CH,
        "vectFrame": IN,  # 0 = XYZ
        "vectOpt": IN,
        "clkAssum": IN,
    },
    "ASHRATT": {
        "msgId": ST,  # "ATT"
        "weekTime": DE,
        "trueHdg": DE,
        "pitch": DE,
        "roll": DE,
        "carrierRmsErr": DE,
        "baselineRmsErr": DE,
        "ambiguity": IN,
    },
    "ASHRBTS": {
        "msgId": ST,  # "BTS"
        "portgroup": (
            3,
            {
                "port": CH,  # C, H or T
                "connected": IN,
                "name": ST,
                "addr": ST,
                "linkQual": IN,
            },
        ),
    },
    "ASHRCAP": {
        "msgId": ST,  # "CAP"
        "name": ST,
        "L1Noffset": DE,
        "L1Eoffset": DE,
        "L1Voffset": DE,
        "L2Noffset": DE,
        "L2Eoffset": DE,
        "L2Voffset": DE,
    },
    "ASHRCPA": {
        "msgId": ST,  # "CPA"
        "antHeight": DE,
        "antRadius": DE,
        "vertOffset": DE,
        "horAzi": DE,
        "horDist": DE,
        "reserved1": ST,
        "reserved2": ST,
        "reserved3": ST,
        "reserved4": ST,
    },
    "ASHRCPO": {
        "msgId": ST,  # "CPO"
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "height": DE,
    },
    "ASHRDDM": {
        "msgId": ST,  # "DDM"
        "corrPort": CH,
        "msgTransport": ST,
        "msgIdent": ST,
        "count": IN,
        "baseId": ST,
        "timeLag": DE,
        "corrAge": DE,
        "attr": ST,
    },
    "ASHRDDS": {
        "msgId": ST,  # "DDS"
        "diffDecodeNum": IN,
        "timeTag": TM,
        "numMsgDecoded": IN,
        "port": CH,
        "prot": ST,
        "timeWindow": IN,
        "percLinkQual": IN,
        "percDeselectInfo": IN,
        "percCrc": IN,
        "latencyStd": IN,
        "latencyMean": IN,
        "epochIntMean": IN,
        "epochIntMin": IN,
        "numMsgDetected": IN,
        "msgType": ST,
        "lastMsgInt": DE,
        "lastMsgAge": DE,
    },
    "ASHRHPR": {
        "msgId": ST,  # "HPR"
        "utctime": TM,
        "trueHdg": DE,
        "pitch": DE,
        "roll": DE,
        "carrierRmsErr": DE,
        "baselineRmsErr": DE,
        "ambiguity": IN,
        "attStatus": IN,
        "antBaseline": ST,
        "PDOP": DE,
    },
    "ASHRLTN": {
        "msgId": ST,  # "LTN"
        "latency": DE,
    },
    "ASHRMDM": {
        "msgId": ST,  # "MDM"
        "port": ST,
        "baud": IN,
        "state": ST,
        "powerMode": ST,
        "pinCode": ST,
        "protocol": IN,
        "csdMode": IN,  # not used
        "accessPoint": ST,
        "login": ST,
        "password": ST,
        "phoneNum": ST,
        "autoDial": CH,
        "maxRedial": IN,
        "model": ST,
        "selMode": IN,
        "gsmAnt": ST,
    },
    "ASHRPBN": {
        "msgId": ST,  # "PBN",
        "gpsWeek": DE,
        "siteName": ST,
        "navX": DE,
        "navY": DE,
        "navT": DE,
        "navXdot": DE,
        "navYdot": DE,
        "navTdot": DE,
        "PDOP": DE,
    },
    "ASHRPOS": {
        "msgId": ST,  # "POS"
        "solnType": IN,
        "sip": IN,
        "utctime": TM,
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "alt": DE,
        "corrAge": DE,
        "trueTrk": DE,
        "sog": DE,
        "vertVel": DE,
        "PDOP": DE,
        "HDOP": DE,
        "VDOP": DE,
        "TDOP": DE,
        "baseId": ST,
    },
    "ASHRPTT": {
        "msgId": ST,  # "PTT"
        "dow": IN,
        "timeTag": ST,
    },
    "ASHRPWR": {
        "msgId": ST,  # "PWR"
        "powerSource": IN,
        "voltsOut": DE,
        "reserved1": ST,
        "percRemaining": IN,
        "reserved2": ST,
        "voltsIn": DE,
        "chargeStatus": IN,
        "reserved3": ST,
        "tempInt": DE,
        "tempBatt": DE,
    },
    "ASHRRCS": {
        "msgId": ST,  # "RCS"
        "recordStatus": CH,
        "memory": IN,
        "fileName": ST,
        "recordRate": IN,
        "occupationType": IN,
        "occupationState": IN,
        "occupationName": ST,
    },
    "ASHRSBD": {
        "msgId": ST,  # "SBD"
        "siv": IN,
        "satgroup": (  # repeating group * siv
            "siv",
            {
                "prn": IN,
                "azi": DE,
                "ele": DE,
                "snrB1": DE,
                "snrB2": DE,
                "snrB3": DE,
                "usageStatus": ST,
                "corrStatus": ST,
            },
        ),
    },
    "ASHRSGA": {
        "msgId": ST,  # "SGA"
        "siv": IN,
        "satgroup": (  # repeating group * siv
            "siv",
            {
                "prn": IN,
                "azi": DE,
                "ele": DE,
                "snrE1": DE,
                "snrE5b": DE,
                "snrE5a": DE,
                "usageStatus": ST,
                "corrStatus": ST,
            },
        ),
    },
    "ASHRSGL": {
        "msgId": ST,  # "SGL"
        "siv": IN,
        "satgroup": (  # repeating group * siv
            "siv",
            {
                "prn": IN,
                "azi": DE,
                "ele": DE,
                "snrL1": DE,
                "snrL2": DE,
                "snrL3": DE,
                "usageStatus": ST,
                "corrStatus": ST,
            },
        ),
    },
    "ASHRSGO": {
        "msgId": ST,  # "SGO"
        "siv": IN,
        "satgroup": (  # repeating group * siv
            "siv",
            {
                "prn": IN,
                "azi": DE,
                "ele": DE,
                "snrE1": DE,
                "snrE5b": DE,
                "snrE5a": DE,
                "snrE6": DE,
                "reserved": ST,
                "usageStatus": ST,
                "corrStatus": ST,
            },
        ),
    },
    "ASHRSGP": {
        "msgId": ST,  # "SGP"
        "siv": IN,
        "satgroup": (  # repeating group * siv
            "siv",
            {
                "prn": IN,
                "azi": DE,
                "ele": DE,
                "snrL1": DE,
                "snrL2": DE,
                "snrL3": DE,
                "usageStatus": ST,
                "corrStatus": ST,
            },
        ),
    },
    "ASHRSIR": {
        "msgId": ST,  # "SIR"
        "siv": IN,
        "satgroup": (  # repeating group * siv
            "siv",
            {
                "prn": IN,
                "azi": DE,
                "ele": DE,
                "reserved2": ST,
                "reserved3": ST,
                "snrL5": DE,
                "usageStatus": ST,
                "corrStatus": ST,
            },
        ),
    },
    "ASHRSLB": {
        "msgId": ST,  # "SLB"
        "siv": IN,
        "satgroup": (  # repeating group * siv
            "siv",
            {
                "satNum": IN,
                "contTrkInt": DE,
                "azi": DE,
                "ele": DE,
                "snr": DE,
            },
        ),
    },
    "ASHRSQZ": {
        "msgId": ST,  # "SQZ"
        "siv": IN,
        "satgroup": (  # repeating group * siv
            "siv",
            {
                "prn": IN,
                "azi": DE,
                "ele": DE,
                "snrL1": DE,
                "snrL2": DE,
                "snrL3": DE,
                "usageStatus": ST,
                "corrStatus": ST,
            },
        ),
    },
    "ASHRSSB": {
        "msgId": ST,  # "SSB"
        "siv": IN,
        "satgroup": (  # repeating group * siv
            "siv",
            {
                "prn": IN,
                "azi": DE,
                "ele": DE,
                "snrL1": DE,
                "reserved": ST,
                "snrL5": DE,
                "usageStatus": ST,
                "corrStatus": ST,
            },
        ),
    },
    "ASHRTEM": {
        "msgId": ST,  # "TEM"
        "temp": DE,  # 1/1000 degrees
    },
    "ASHRTHS": {
        "msgId": ST,  # "THS"
        "lastComputedHdg": DE,
        "solnStatus": CH,
    },
    "ASHRTTT": {
        "msgId": ST,  # "TTT"
        "dow": IN,
        "timeTag": TM,
    },
    "ASHRVCR": {
        "msgId": ST,  # "VCR"
        "baselineNum": IN,
        "baselineMode": IN,
        "sip": IN,
        "utctime": TM,
        "antEcefX": DE,
        "antEcefY": DE,
        "antEcefZ": DE,
        "coord1std": DE,
        "coord2std": DE,
        "coord3std": DE,
        "coord12corr": DE,
        "coord13corr": DE,
        "coord23corr": DE,
        "baseId": ST,
        "baselineCoordId": ST,  # 0 = XYZ
    },
    "ASHRVCT": {
        "msgId": ST,  # "VCT"
        "baselineMode": IN,
        "sip": IN,
        "utctime": TM,
        "antEcefX": DE,
        "antEcefY": DE,
        "antEcefZ": DE,
        "coord1std": DE,
        "coord2std": DE,
        "coord3std": DE,
        "coord12corr": DE,
        "coord13corr": DE,
        "coord23corr": DE,
        "baseId": ST,
        "baselineCoordId": ST,  # 0 = XYZ
        "baselineNum": IN,
        "vrs": IN,
        "staticModeAssumption": IN,
    },
    "ASHRVEL": {
        "msgId": ST,  # "VEL"
        "velE": DE,
        "velN": DE,
        "velV": DE,
        "velERmsErr": DE,
        "velNRmsErr": DE,
        "velVRmsErr": DE,
        "velSmoothInt": IN,
    },
    "FUGDP": {
        "type": ST,  # GPS (GP), GLONASS (GL) or GNSS (GN)
        "utctime": TM,
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "siv": IN,
        "dpvoaQual": ST,
        "dgnssMode": ST,
        "smajErr": DE,
        "sminErr": DE,
        "dirErr": IN,
    },
    "GPPADV110": {
        "msgId": ST,  # "110"
        "lat": DE,
        "lon": DE,
        "height": DE,
        "ele": DE,  # optional
        "azi": DE,  # optional
    },
    "GPPADV120": {
        "msgId": ST,  # "120"
        "satgrp": (  # repeating group * 2
            2,
            {
                "prn": IN,
                "ele": DE,
                "azi": DE,
            },
        ),
    },
    "TNLAVR": {
        "msgId": ST,  # "AVR"
        "utctime": TM,
        "yaw": DE,
        "yawc": ST,  # "Yaw"
        "tilt": DE,
        "tiltc": ST,  # "Tilt"
        "roll": DE,
        "rollc": ST,  # "Roll"
        "range": DE,
        "gpsQual": IN,
        "PDOP": DE,
        "sip": IN,
    },
    "TNLBPQ": {
        "msgId": ST,  # "BPQ"
        "utctime": TM,
        "utcdate": DT,
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "height": ST,  # starts with "EHT-"
        "hunit": CH,  # 'M'
        "gpsQual": IN,
    },
    "TNLDG": {
        "msgId": ST,  # "DG" TODO check
        "strength": DE,
        "snr": DE,
        "freq": DE,
        "bitRate": IN,
        "chan": IN,
        "trkStatus": CH,
        "trkPerf": IN,
    },
    "TNLEVT": {
        "msgId": ST,  # "EVT"
        "utctime": TM,
        "port": IN,
        "numEvents": IN,
        "wno": IN,
        "dow": IN,
        "leaps": IN,
    },
    "TNLGGK": {
        "msgId": ST,  # "GGK"
        "utctime": TM,
        "utcdate": DT,
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "gpsQual": IN,
        "sip": IN,
        "DOP": DE,
        "height": ST,  # starts with "EHT-"
        "hunit": CH,  # 'M'
    },
    "TNLGGKx": {
        "msgId": ST,  # "GGK"
        "utctime": TM,
        "utcdate": DT,
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "posType": IN,
        "sip": IN,
        "PDOP": DE,
        "height": DE,
        "numExt": IN,
        "sigmaE": DE,
        "sigmaN": DE,
        "sigmaV": DE,
        "propogationAge": DE,
    },
    "TNLPJK": {
        "msgId": ST,  # "PJK"
        "utctime": TM,
        "utcdate": DT,
        "northing": DE,
        "nunit": CH,  # 'N'
        "easting": DE,
        "eunit": CH,  # 'E"
        "gpsQual": IN,
        "sip": IN,
        "DOP": DE,
        "height": ST,  # starts with "EHT-" or "GHT-"
        "hunit": CH,  # 'M'
    },
    "TNLPJT": {
        "msgId": ST,  # "PJT"
        "coordName": ST,
        "projName": ST,
    },
    "TNLREX": {
        "msgId": ST,  # "REX"
        "utctime": TM,
        "constUsed": ST,
        "sip": IN,
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "alt": DE,
        "latSigmaErr": DE,
        "lonSigmaErr": DE,
        "heightSigmaErr": DE,
        "vectE": DE,
        "vectN": DE,
        "vectV": DE,
        "vectESigmaErr": DE,
        "vectNSigmaErr": DE,
        "vectVSigmaErr": DE,
        "corrSource": ST,
    },
    "TNLVGK": {
        "msgId": ST,  # "VGK"
        "utctime": TM,
        "utcdate": DM,  # mmddyy
        "vectE": DE,
        "vectN": DE,
        "vectV": DE,
        "gpsQual": IN,
        "sip": IN,
        "DOP": DE,
        "vunit": CH,  # 'M'
    },
    "TNLVHD": {
        "msgId": ST,  # "VHD"
        "utctime": TM,
        "utcdate": DM,  # mmddyy
        "azi": DE,
        "aziRate": DE,
        "ele": DE,
        "eleRate": DE,
        "range": DE,
        "rangeRate": DE,
        "gpsQual": IN,
        "sip": IN,
        "PDOP": DE,
        "unit": CH,  # 'M'
    },
    # *********************************************
    # Furuno
    # https://www.furuno.com/en/support/sdk/
    # *********************************************
    "FECGPATT": {
        "msgId": ST,  # 'GPatt'
        "yaw": DE,
        "pitch": DE,
        "roll": DE,
    },
    "FECGPHVE": {
        "msgId": ST,  # 'GPhve'
        "heave": DE,
        "status": CH,  # 'A'
    },
    # ***************************************************************
    # Locosys Proprietary Messages GET
    # https://www.locosystech.com/Templates/att/LS2303x-UDG_datasheet_v0.6.pdf?lng=en
    # ***************************************************************
    "LSR": {
        "msgType": ST,  # e.g. "SLOPE", "MEMS", "ATTIT"
        "value": IN,  # e.g. 0
        "response": ST,  # e.g. "OK"
    },
    "LSVD": {
        "velE": DE,  # cm/s
        "velN": DE,  # cm/s
        "velD": DE,  # cm/s
        "velEdev": DE,  # cm/s deviation
        "velNdev": DE,  # cm/s deviation
        "velDdev": DE,  # cm/s deviation
    },
    "INVMINR": {
        "status": CH,  # 0 uninitialized; 1、2 calibrating/initializing; 3 calibration done
    },
    "INVMSTR": {
        "value": IN,
    },
    "INVMSLOPE": {
        "slope": DE,  # degrees
        "altDiff": DE,  # meters
        "moveDist": DE,  # meters
        "slopeAccu": DE,  # degrees
        "altDiffAccu": DE,  # meters
        "moveDistAccu": DE,  # meters
    },
    "INVMIMU": {
        "timeSecond": DE,  # sec timestamp
        "accelX": DE,  # m/s^2
        "accelY": DE,  # m/s^2
        "accelZ": DE,  # m/s^2
        "gyroX": DE,  # degree/s
        "gyroY": DE,  # degree/s
        "gyroZ": DE,  # degree/s
    },
    "INVMATTIT": {
        "roll": DE,  # degree
        "pitch": DE,  # degree
        "yaw": DE,  # degree heading
    },
    # ***************************************************************
    # Quectel LC29H / LC79H Proprietary GET message types
    # https://www.quectel.com/download/quectel_lc29hlc79h_series_gnss_protocol_specification_v1-5/
    # quectel_lc29hlc79h_series_gnss_protocol_specification_v1-5.pdf
    # ***************************************************************
    "AIR001": {
        "commandid": IN,
        "result": IN,
    },
    "AIR010": {
        "type": IN,
        "subsystem": IN,
        "wno": IN,
        "tow": IN,
    },
    "AIR051": {
        "time": IN,
    },
    "AIR059": {
        "minsnr": IN,
    },
    "AIR063": {
        "type": IN,
        "rate": IN,
    },
    "AIR067": {
        "gpsEnabled": IN,
        "glonassEnabled": IN,
        "galileoEnabled": IN,
        "bdsEnabled": IN,
        "qzssEnabled": IN,
        "navicEnabled": IN,
    },
    "AIR071": {
        "speedThreshold": DE,
    },
    "AIR073": {
        "degree": IN,
    },
    "AIR075": {
        "enabled": IN,
    },
    "AIR081": {
        "navMode": IN,
    },
    "AIR087": {
        "status": IN,
    },
    "AIR101": {
        "nmeaMode": IN,
        "reserved": IN,
    },
    "AIR105": {
        "dualBandEnabled": IN,
    },
    "AIR391": {
        "cmdType": IN,
    },
    "AIR401": {
        "mode": IN,
    },
    "AIR411": {
        "enabled": IN,
    },
    "AIR421": {
        "enabled": IN,
    },
    "AIR433": {
        "mode": IN,
    },
    "AIR435": {
        "enabled": IN,
    },
    "AIR436": {
        "enabled": IN,
    },
    "AIR437": {"enabled": IN},
    "AIR491": {
        "enabled": IN,
    },
    "AIR650": {
        "second": IN,
    },
    "AIR865": {
        "baudrate": IN,
    },
    "AIR867": {
        "flowControl": IN,
    },
    "AIR6011": {
        "type": IN,
        "rate": IN,
    },
    "AIRSPF": {
        "status": IN,
    },
    "AIRSPF5": {
        "status": IN,
    },
    # ***************************************************************
    # Quectel LG290P Proprietary message types
    # https://quectel.com/content/uploads/2024/09/Quectel_LG290P03_GNSS_Protocol_Specification_V1.0.pdf
    #
    # status attribute must be set to:
    # 'R' for POLL messages (queries)
    # 'W' for SET messages (commands)
    # 'OK' for GET acknowledgements (ACK)
    # 'ERROR' for GET errors (NAK)
    # ***************************************************************
    "QTMACK": {
        "status": QS,  # OK
    },
    "QTMNAK": {
        "status": QS,  # ERROR
        "errcode": IN,  # 1 = invalid parms, 2 = failed exec, 3 = unsupported
    },
    "QTMANTENNASTATUS": {
        "msgver": IN,  # always 1 for this version
        "antennastatus": IN,
        "antennapowerind": IN,
    },
    "QTMCFGAIC": {
        "status": QS,
        "state": IN,
    },
    "QTMCFGANTDELTA": {
        "status": QS,
        "east": DE,
        "north": DE,
        "height": DE,
    },
    "QTMCFGANTINF": {
        "status": QS,
        "antennadesc": ST,
        "antennasetupid": IN,
        "antennasn": ST,
    },
    "QTMCFGBLD": {
        "status": QS,
        "distance": DE,
    },
    "QTMCFGCNST": {
        "status": QS,
        "gps": IN,
        "glonass": IN,
        "galileo": IN,
        "beidou": IN,
        "qzss": IN,
        "navic": IN,
    },
    "QTMCFGDR": {
        "status": QS,
        "drstate": IN,
    },
    "QTMCFGDRHOT": {"status": QS, "mode": IN},
    "QTMCFGDRRTD": {"status": QS, "time": IN, "distance": IN},
    "QTMCFGEINSMSG": {
        "type": IN,
        "ins_enabled": IN,
        "imu_enabled": IN,
        "gps_enabled": IN,
        "rate": IN,
    },
    "QTMCFGELETHD": {
        "status": QS,
        "elevation": DE,
    },
    "QTMCFGFIXRATE": {
        "status": QS,
        "fixinterval": IN,
    },
    "QTMCFGGEOFENCE": {
        "status": QS,
        "geofenceindex": IN,
        "geofencemode": IN,
        "reserved": IN,
        "shape": IN,
        "lat0": DE,
        "lon0": DE,
        "radiuslat1": DE,  # use for radius or lat1
    },
    "QTMCFGGEOFENCE_DIS": {
        "status": QS,
        "geofenceindex": IN,
        "geofencemode": IN,  # should be 0
    },
    "QTMCFGGEOFENCE_POLY": {
        "status": QS,
        "geofenceindex": IN,
        "geofencemode": IN,
        "reserved": IN,
        "shape": IN,
        "lat0": DE,
        "lon0": DE,
        "radiuslat1": DE,  # use for radius or lat1
        "lon1": DE,
        "lat2": DE,
        "lon2": DE,
        "lat3": DE,
        "lon3": DE,
    },
    "QTMCFGGEOSEP": {
        "status": QS,
        "mode": IN,
        "geosep": DE,
    },
    "QTMCFGIMUINT": {
        "status": QS,
        "index": IN,
        "mode": IN,
        "reserved": IN,
        "actLevel": IN,
    },
    "QTMCFGIMUTC": {
        "status": QS,
        "imustatus": IN,
    },
    "QTMCFGLA": {
        "status": QS,
        "type": IN,
        "laX": DE,
        "laY": DE,
        "laZ": DE,
    },
    "QTMCFGLAM": {
        "status": QS,
        "mode": IN,
    },
    "QTMCFGMSGRATE": {
        "status": QS,
        "msgname": ST,
        "rate": IN,
        "msgver": IN,  # or offset
    },
    "QTMCFGMSGRATE_NOVER": {
        "status": QS,
        "msgname": ST,
        "rate": IN,
    },
    "QTMCFGMSGRATE_INTF": {
        "status": QS,
        "porttype": IN,  # 1 = UART
        "portid": IN,  # 1 =UART1, 2 = UART2, 3 = UART3
        "msgname": ST,
        "rate": IN,
        "msgver": IN,  # or offset
    },
    "QTMCFGMSGRATE_INTFNOVER": {
        "status": QS,
        "porttype": IN,  # 1 = UART
        "portid": IN,  # 1 =UART1, 2 = UART2, 3 = UART3
        "msgname": ST,
        "rate": IN,
    },
    "QTMCFGNAVMODE": {
        "status": QS,
        "mode": IN,
    },
    "QTMCFGNMEADP": {
        "status": QS,
        "utcdp": IN,
        "posdp": IN,
        "altdp": IN,
        "dopdp": IN,
        "spddp": IN,
        "cogdp": IN,
    },
    "QTMCFGNMEATID": {
        "status": QS,
        "mainTalker": ST,
        "gsvTalker": ST,
    },
    "QTMCFGODO": {
        "status": QS,
        "state": IN,  # 0 disabled, 1 enabled
        "initdist": DE,
    },
    "QTMCFGPPS": {
        "status": QS,
        "ppsindex": IN,
        "enable": IN,
        "duration": IN,
        "ppsmode": IN,
        "polarity": IN,
        "reserved": IN,
    },
    "QTMCFGPROT": {
        "status": QS,
        "porttype": IN,
        "portid": IN,
        "inputprot": ST,  # 8 hex digits
        "outputprot": ST,  # 8 hex digits
    },
    "QTMCFGRCVRMODE": {
        "status": QS,
        "rcvrmode": IN,  # 0 unknown, 1 rover, 2 base
    },
    "QTMCFGRSID": {
        "status": QS,
        "rsid": IN,
    },
    "QTMCFGRTCM": {
        "status": QS,
        "msmtype": IN,
        "msmmode": IN,
        "msmelevthd": DE,
        "reserved1": ST,  # must be 07 with leading 0
        "reserved2": ST,  # must be 06 with leading 0
        "ephmode": IN,
        "ephinterval": IN,
    },
    "QTMCFGRTK": {
        "status": QS,
        "diffmode": IN,  # 0 disable, 1 auto, 2 RTD only
        "relmode": IN,  # 1 absolute, 2 relative
    },
    "QTMCFGRTKSRCTYPE": {
        "status": QS,
        "srctype": IN,
    },
    "QTMMCFGRTKSRCTYPE": {
        "status": QS,
        "srctype": IN,
    },
    "QTMCFGSAT": {
        "status": QS,
        "systemid": IN,
        "signalid": ST,  # hex as string
        "masklow": ST,  # hex as string
        "maskhigh": ST,  # hex as string
    },
    "QTMCFGSAT_LOW": {
        "status": QS,
        "systemid": IN,
        "signalid": ST,  # hex as string
        "masklow": ST,  # hex as string
    },
    "QTMCFGSBAS": {
        "status": QS,
        "value": HX,
    },
    "QTMCFGSIGGRP": {
        "status": QS,
        "siggrpnum": IN,
    },
    "QTMCFGSIGNAL": {
        "status": QS,
        "gpssig": ST,  # hex as string, default 07
        "glonasssig": ST,  # hex as string, default 03
        "galileosig": ST,  # hex as string, default 0F
        "beidousig": ST,  # hex as string, default 3F
        "qzsssig": ST,  # hex as string, default 07
        "navicsig": ST,  # hex as string, default 01
    },
    "QTMCFGSIGNAL2": {
        "status": QS,
        "gpssig": ST,  # hex as string, default 07
        "glonasssig": ST,  # hex as string, default 03
        "galileosig": ST,  # hex as string, default 0F
        "beidousig": ST,  # hex as string, default 3F
        "qzsssig": ST,  # hex as string, default 07
        "navicsig": ST,  # hex as string, default 01
    },
    "QTMCFGSTATICHOLD": {
        "status": QS,
        "shstate": IN,
    },
    "QTMCFGSVIN": {
        "status": QS,
        "svinmode": IN,
        "cfgcnt": IN,
        "acclimit": DE,
        "ecefx": DE,
        "ecefy": DE,
        "ecefz": DE,
    },
    "QTMCFGUART": {
        "status": QS,
        "portid": IN,
        "baudrate": IN,
        "databit": IN,
        "parity": IN,
        "stopbit": IN,
        "flowctrl": IN,
    },
    "QTMCFGVEHMOT": {
        "status": QS,
        "mode": IN,
        "vehtype": IN,
    },
    "QTMCFGWN": {
        "status": QS,
        "weekno": IN,
    },
    "QTMDEBUGON": {"status": QS},
    "QTMDEBUGOFF": {"status": QS},
    "QTMDOP": {
        "msgver": IN,  # always 1 for this version
        "tow": IN,
        "gdop": DE,
        "pdop": DE,
        "tdop": DE,
        "vdop": DE,
        "hdop": DE,
        "ndop": DE,
        "edop": DE,
    },
    "QTMDRCAL": {
        "msgver": IN,  # always 1 for this version
        "calstate": IN,  # 0 = none, 1 = lightly, 2 = fully
        "navtype": IN,  # 0 = none, 1 = GNSS only, 2 = DR only, 3 = GNSS + DR
    },
    "QTMDRCLR": {"status": QS},
    "QTMDRPVA": {
        "msgver": IN,  # always 1 for this version
        "timestamp": IN,
        "time": DE,
        "solType": IN,
        "lat": DE,
        "lon": DE,
        "alt": DE,
        "sep": DE,
        "velN": DE,
        "velE": DE,
        "velD": DE,
        "speed": DE,
        "roll": DE,
        "pitch": DE,
        "heading": DE,
    },
    "QTMDRSAVE": {"status": QS},
    "QTMEOE": {
        "msgver": IN,  # always 2 for this version
        "utc": DE,
        "Date": IN,
        "WN": IN,
        "TOW": IN,
    },
    "QTMEPE": {
        "msgver": IN,  # always 2 for this version
        "epenorth": DE,
        "epeeast": DE,
        "epedown": DE,
        "epe2d": DE,
        "epe3d": DE,
    },
    "QTMGEOFENCESTATUS": {"msgver": IN, "time": TM, "group": (4, {"staten": IN})},
    "QTMGETUTC": {
        "status": QS,
        "year": IN,
        "month": IN,
        "day": IN,
        "hour": IN,
        "minute": IN,
        "second": IN,
        "millisecond": IN,
        "reserved": ST,
        "leapsecond": IN,
    },
    "QTMGNSSSTART": {"status": QS},
    "QTMGNSSSTOP": {"status": QS},
    "QTMGPS": {
        "timestamp": IN,
        "tow": IN,
        "lat": DE,
        "lon": DE,
        "alt": DE,
        "speed": DE,
        "heading": DE,
        "accuracy": DE,
        "HDOP": DE,
        "PDOP": DE,
        "numSv": IN,
        "fixMode": IN,
    },
    "QTMJAMMINGSTATUS": {
        "msgver": IN,  # always 1 for this version
        "jammingstatus": IN,
    },
    "QTMIMU": {
        "timestamp": IN,
        "accX": DE,
        "accY": DE,
        "accZ": DE,
        "angrateX": DE,
        "angrateY": DE,
        "angrateZ": DE,
        "wheeltick": IN,
        "last_tick_timestamp": IN,
    },
    "QTMIMUTYPE": {
        "msgver": IN,  # always 1 for this version
        "imustatus": IN,  # 0 = failed, 1 = OK
    },
    "QTMINS": {
        "timestamp": IN,
        "soltype": IN,
        "lat": DE,
        "lon": DE,
        "height": DE,
        "velN": DE,
        "velE": DE,
        "velD": DE,
        "roll": DE,
        "pitch": DE,
        "yaw": DE,
    },
    "QTMLS": {
        "msgver": IN,  # always 1 for this version
        "tow": IN,
        "lsRef": HX,
        "wno": IN,
        "leapsecond": IN,
        "flag": IN,
        "lsfRef": HX,
        "reserved": ST,
        "wnlsf": IN,
        "dn": IN,
        "lsf": IN,
    },
    "QTMNAV": {
        "msgver": IN,  # always 1 for this version
        "timestatus": IN,
        "timeref": IN,
        "utc": DE,
        "date": IN,
        "tow": IN,
        "wn": IN,
        "leapsec": IN,
        "reserved1": ST,
        "reserved2": ST,
        "soltype": IN,
        "reserved3": IN,
        "lat": DE,
        "lon": DE,
        "alt": DE,
        "sep": DE,
        "reserved4": ST,
        "reserved5": ST,
        "latstd": DE,
        "lonstd": DE,
        "altstd": DE,
        "reserved6": ST,
        "reserved7": ST,
        "diffid": DE,
        "diffAge": DE,
        "reserved8": ST,
        "siv": IN,
        "sip": IN,
        "reserved9": ST,
        "reserved10": ST,
        "reserved11": ST,
        "reserved12": ST,
        "reserved13": ST,
        "reserved14": ST,
        "hvel": DE,
        "vvel": DE,
        "hvelstd": DE,
        "vvelstd": DE,
        "reserved15": ST,
        "reserved16": ST,
        "cog": DE,
        "reserved17": ST,
        "reserved18": ST,
    },
    "QTMODO": {
        "msgver": IN,  # always 1 for this version
        "time": TM,
        "state": IN,  # 0 disabled, 1 enabled
        "dist": DE,
    },
    "QTMPL": {
        "msgver": IN,  # always 1 for this version
        "tow": IN,
        "pul": DE,
        "reserved1": IN,
        "reserved2": IN,
        "plposn": DE,
        "plpose": DE,
        "plposd": DE,
        "plveln": DE,
        "plvele": DE,
        "plveld": DE,
        "reserved3": IN,
        "reserved4": IN,
        "pltime": IN,
    },
    "QTMPVT": {
        "msgver": IN,  # always 1 for this version
        "tow": IN,
        "date": ST,  # yyyymmdd
        "time": TM,
        "reserved": IN,
        "fixtype": IN,
        "numsv": IN,
        "leaps": IN,
        "lat": DE,
        "lon": DE,
        "alt": DE,
        "sep": DE,
        "veln": DE,
        "vele": DE,
        "veld": DE,
        "spd": DE,
        "hdg": DE,
        "hdop": DE,
        "pdop": DE,
    },
    "QTMQVER": {
        "status": QS,
        "msgver": IN,
        "description": ST,
        "version": ST,
        "buildDate": ST,
        "buildTime": ST,
    },
    "QTMRESETODO": {"status": QS},
    "QTMRESTOREPAR": {"status": QS},
    "QTMSAVEPAR": {"status": QS},
    "QTMSENMSG": {
        "msgver": IN,  # 2 or 4
        "timestamp": IN,
        "group": (
            "None",
            {
                "sensor_info": DE,
            },
        ),
    },
    "QTMSN": {
        "status": QS,
        "snid": IN,  # fixed to 1
        "length": IN,
        "serialno": ST,
    },
    "QTMSN_ALT": {
        "snid": IN,  # fixed to 1
        "length": IN,
        "status": QS,
        "serialno": ST,
    },
    "QTMSTD": {
        "reserved": ST,
        "utc": TM,
        "wno": IN,
        "tow": IN,
        "stdLat": ST,  # defined as ST as fields can be blank
        "stdLon": ST,
        "stdAlt": ST,
        "stdSep": ST,
        "stdVelN": ST,
        "stdVelE": ST,
        "stdVelD": ST,
        "stdSpd": ST,
        "stdRoll": ST,
        "stdPitch": ST,
        "stdHeading": ST,
    },
    "QTMSVINSTATUS": {
        "msgver": IN,  # always 1 for this version
        "tow": IN,
        "valid": IN,
        "reserved0": IN,
        "reserved1": IN,
        "obs": IN,
        "cfgdur": IN,
        "meanx": DE,
        "meany": DE,
        "meanz": DE,
        "meanacc": DE,
    },
    "QTMTAR": {
        "msgver": IN,  # always 1 for this version
        "time": DE,
        "quality": DE,
        "res": DE,
        "length": DE,
        "pitch": DE,
        "roll": DE,
        "heading": DE,
        "accpitch": DE,
        "accroll": DE,
        "accheading": DE,
        "usedsv": IN,
    },
    "QTMTXT": {
        "msgver": IN,  # always 1 for this version
        "totalsennum": IN,
        "sennum": IN,
        "textid": IN,
        "text": ST,
    },
    "QTMUNIQID": {
        "status": QS,
        "length": IN,
        "ID": HX,
    },
    "QTMVEHATT": {
        "msgver": IN,  # always 1 for this version
        "timestamp": IN,
        "roll": DE,
        "pitch": DE,
        "heading": DE,
        "acc_Roll": DE,
        "acc_Pitch": DE,
        "acc_Heading": DE,
    },
    "QTMVEHMOT": {
        "msgver": IN,  # 1 or 2
        "group": (
            "None",
            {
                "vehicle_info": DE,
            },
        ),
    },
    "QTMVEHMSG": {
        "msgver": IN,  # 1 = speed, 2 = tick, 3 = speed 4wd, 4 = ticks 4wd
        "timestamp": IN,
        "group": (
            "None",
            {
                "vehicle_info": DE,
            },
        ),
    },
    "QTMVEL": {
        "msgver": IN,  # always 1 for this version
        "time": TM,
        "veln": DE,
        "vele": DE,
        "veld": DE,
        "gndspd": DE,
        "spd": DE,
        "hdg": DE,
        "gndspdacc": DE,
        "spdacc": DE,
        "hdgacc": DE,
    },
    "QTMVER": {
        "msgver": IN,  # always 1 for this version
        "vername": ST,
        "verstr": ST,
        "builddate": ST,  # yyyy/mm/dd
        "buildtime": ST,  # hh:mm:ss
    },
    "QTMVERNO": {
        "verstr": ST,
        "builddate": ST,  # yyyy/mm/dd
        "buildtime": ST,  # hh:mm:ss
    },
    # ***************************************************************
    # Quectel LG69T PSTM Proprietary message types
    # https://quectel.com/content/uploads/2024/09/quectel_lg69taaadafaiajar_gnss_protocol_specification_v1-5.pdf
    # ***************************************************************
    "STMPPSDATA": {
        "onoff": IN,
        "ppsvalid": IN,
        "syncvalid": IN,
        "outmode": IN,
        "reftime": IN,
        "refconst": IN,
        "pulseduration": DE,  # second pulse duration.
        "pulsedelay": DE,  # nanosecond pulse delay.
        "gpsdelay": DE,  # nanosecond gps path rf delay.
        "reserved1": ST,
        "bdsdelay": DE,  # nanosecond bds path rf delay.
        "galileodelay": DE,  # nanosecond galileo path rf delay.
        "invertedpolarity": IN,
        "fixcond": IN,
        "satth": DE,
        "elevmask": DE,
        "constmask": IN,
        "refsec": DE,  # second
        "fixstatus": DE,
        "usedsats": DE,  #  used satellites for time correction.
        "gpsutcdeltas": DE,  # second utc leap seconds.
        "gpsutcdeltans": DE,  # nanosecond utc–gps delta time.
        "reserved2": ST,
        "galileoutcdeltans": DE,  # nanosecond utc–galileo delta time.
        "quantizationerror": DE,  # second quantization error.
        "ppsclockfreq": DE,  # hz pps clock frequency.
        "tcxoclockfreq": DE,  # hz tcxo clock frequency.
        "bdsutcdeltatimes": DE,  # second utc–bds leap second.
    },
    "STMCPU": {
        "cpuusage": DE,  #  cpu usage in percentage (%).
        "pllonoff": IN,
        "cpuspeed": HX,  # hexadecimal mhz cpu clock frequency.
    },
    "STMTG": {
        "wno": IN,  #  week number.
        "tow": DE,  # second time of week.
        "reserved1": ST,  # reserved
        "cputime": DE,  #  cpu time.
        "timevalid": IN,
        "nco": DE,  # hz
        "configstatus": HX,  # hexadecimal
        "constmask": IN,
        "timebestsattype": IN,  #  selected best time satellite type.
        "timemastersattype": IN,  #  master time satellite type.
        "timemasterwn": IN,  #  master time week number.
        "timemastertow": DE,  # second master time tow.
        "timemastervalidity": DE,  # master week number time validity.
        "tgauxflags": IN,
        "clockbias": DE,  # meter estimated receiver clock bias.
        "mfreqconfigmask": DE,  #  multifrequency configuration mask.
        "leapsec": IN,  # second
        "ppsedge": DE,  #  pps edge counter @ 64f0 resolution.
        "mtbms": DE,  # millisecond
        "mtbtimestamp": DE,  # picosecond
    },
    "STMTS": {
        "dspdat": IN,
        "satid": IN,  #  satellite identifier.
        "psr": DE,  # meter pseudo range.
        "freq": DE,  #  satellite tracking frequency offset.
        "cp": DE,  # cycle carrier phase measurement.
        "dspflags": IN,
        "satcn0": DE,  # dbhz satellite carrier to noise ratio.
        "ttim": DE,  # second track time of satellite.
        "codenoise": DE,
        "phasenoise": DE,
        "cycleslipcnt": DE,  #  total cycle slip counter.
        "reserved1": ST,
        "elev": DE,  # degree elevation degree.
    },
    "STMSBAS": {
        "status": IN,
        "sattrk": IN,
        "satid": IN,  #  sbas satellite id.
        "elev": DE,  # degree sbas satellite elevation.
        "azim": DE,  # degree sbas satellite azimuth.
        "satcn0": DE,  # dbhz sbas satellite signal strength c/n0.
    },
    "STMTEMP": {
        "temperature": DE,
        "rawtemperature": DE,
        "calibration": IN,
    },
    "STMDRCONFID": {
        "latstddev": DE,  # meter latitude standard deviation.
        "lonstddev": DE,  # meter longitude standard deviation.
        "headingstddev": DE,  # degree heading standard deviation.
        "reserved1": ST,
        "gyrobiasstddev": DE,  # millivolt gyroscope bias standard deviation.
        "odoscalestddev": DE,  # millimeter/pulse odometer scale standard deviation.
        "reserved2": ST,
        "accoffsetstddev": DE,  # g accelerometer offset standard deviation.
        "heightstddev": DE,  # meter height standard deviation.
        "majorsemiaxis": DE,  # meter major semiaxis of 1sigma error ellipse.
        "minorsemiaxis": DE,  # meter minor semiaxis of 1sigma error ellipse.
        "ellipseangle": DE,  # degree angle vs north of 1sigma error ellipse.
        "speedstddev": DE,  # m/s speed standard deviation.
    },
    "STMDRBSD": {
        "timestamp": DE,
        "cputime": IN,  #  time of dr estimation (cpu ticks).
        "gyroxbiassd": DE,  # dps gyroscope x bias standard deviation.
        "gyroybiassd": DE,  # dps gyroscope y bias standard deviation.
        "gyrozbiassd": DE,  # dps gyroscope z bias standard deviation.
        "accxbiassd": DE,  # m/s2 accelerometer x bias standard deviation.
        "accybiassd": DE,  # m/s2 accelerometer y bias standard deviation.
        "acczbiassd": DE,  # m/s2 accelerometer z bias standard deviation.
    },
    "STMDRGPS": {
        "lat": DE,  # degree gnss latitude.
        "lon": DE,  # degree gnss longitude.
        "vn": DE,  # m/s gnss velocity north component.
        "ve": DE,  # m/s gnss velocity east component.
        "pdop": DE,
        "hdop": DE,
        "vdop": DE,
        "rmsposresidual": DE,  # meter rms error on gnss pseudo range measurements.
        "rmsvelresidual": DE,  # m/s rms error on gnss frequency measurements.
        "vup": DE,  # m/s gnss velocity up component.
        "height": DE,  # meter gnss altitude.
    },
    "STMDRPVA": {
        "timestamp": DE,
        "cputime": IN,  # microsecond time of dr estimation (cpu ticks).
        "latitude": DE,  # degree dr latitude.
        "longitude": DE,  # degree dr longitude.
        "height": DE,  # meter dr height.
        "vnorth": DE,  # m/s dr velocity north component.
        "veast": DE,  # m/s dr velocity east component.
        "vup": DE,  # m/s dr velocity up component.
        "pitch": DE,  # degree dr pitch angle. range: 90.00 to 90.00.
        "roll": DE,  # degree dr roll angle. range: 180.00 to 180.00.
        "heading": DE,  # degree dr heading angle. range: 0.00 to 360.00.
    },
    "STMDRPVASD": {
        "timestamp": DE,
        "cputime": IN,  # microsecond time of dr estimation (cpu ticks).
        "latitudesd": DE,  # degree dr latitude standard deviation.
        "longitudesd": DE,  # degree dr longitude standard deviation.
        "heightsd": DE,  # meter dr height standard deviation.
        "vnorthsd": DE,  # m/s dr velocity north component standard deviation.
        "veastsd": DE,  # m/s dr velocity east component standard deviation.
        "vupsd": DE,  # m/s dr velocity up component standard deviation.
        "pitchsd": DE,  # degree dr pitch angle standard deviation.
        "rollsd": DE,  # degree dr roll angle standard deviation.
        "headingsd": DE,  # degree dr heading angle standard deviation.
        "pnesd": DE,  # meter dr position north east standard deviation.
        "pnusd": DE,  # meter dr position north up standard deviation.
        "peusd": DE,  # meter dr position east up standard deviation.
        "vnesd": DE,  # m/s dr velocity north east standard deviation.
        "vnusd": DE,  # m/s dr velocity north up standard deviation.
        "veusd": DE,  # m/s dr velocity east up standard deviation.
    },
    "STMDRSINT": {
        "gyrosamplecount": IN,  #  number of received gyroscope samples.
        "accsamplecount": IN,  #  number of received accelerometer samples.
        "pressamplecount": IN,  #  number of received pressure samples.
        "odometercount": IN,  #  number of received odometer pulses.
        "gyrointtime": DE,  # second
        "accinttime": DE,  # second
        "pressureinttime": DE,  # second
        "gyroxavg": DE,  # dps
        "gyroyavg": DE,  # dps
        "gyrozavg": DE,  # dps
        "accxavg": DE,  # m/s2
        "accyavg": DE,  # m/s2
        "acczavg": DE,  # m/s2
        "presavg": DE,  # hpa average of received pressure samples.
    },
    "STMDRSVF": {
        "timestamp": DE,
        "cputime": IN,  # microsecond time of estimation (cpu ticks).
        "xacceleration": DE,  # m/s2 vehicle acceleration in x direction.
        "yacceleration": DE,  # m/s2 vehicle acceleration in y direction.
        "zacceleration": DE,  # m/s2 vehicle acceleration in z direction.
        "xangularrate": DE,  # dps vehicle angular rate in x direction.
        "yangularrate": DE,  # dps vehicle angular rate in y direction.
        "zangularrate": DE,  # dps vehicle angular rate in z direction.
    },
    "STMDRUPD": {"group": ("None", {"data": HX})},
    "STMDRSTYPE": {
        "sensortype": IN,
    },
    "STMDRCAL": {
        "driscalib": IN,
        "odoiscalib": IN,
        "gyrosensitivityiscalib": IN,
        "gyrobiasiscalib": IN,
        "imuflag": HX,
        "gyrointegrityflag": IN,
        "accintegrity": IN,
        "calstate": ST,
    },
    "STMDR1": {
        "mpitch": DE,  # degree misalignment sensor vs. vehicle frame – pitch angle.
        "mroll": DE,  # degree misalignment sensor vs. vehicle frame – roll angle.
        "myaw": DE,  # degree misalignment sensor vs. vehicle frame – yaw angle.
        "gsz": DE,  #  gyroscope z axis sensitivity.
        "gbx": DE,  # dps gyroscope x axis bias.
        "gby": DE,  # dps gyroscope y axis bias.
        "gbz": DE,  # dps gyroscope z axis bias.
        "abx": DE,  # m/s2 accelerometer x axis bias.
        "aby": DE,  # m/s2 accelerometer y axis bias.
        "abz": DE,  # m/s2 accelerometer z axis bias.
        "odometerscale": DE,  # meter/pulse odometer scale.
        "res1baro": DE,  #  reserved for barometer.
        "res2baro": DE,  #  reserved for barometer.
    },
    "STMDR2": {
        "imucal": ST,
        "ascal": ST,
        "motionstatus": IN,
        "errcode": IN,
        "sysready": IN,
        "crosstrackerror": DE,  # meter crosstrack error vs gnssonly mode.
        "alongtrackerror": DE,  # meter alongtrack error vs gnssonly mode.
        "sysaligned": IN,
        "vrows": DE,  # meter estimated vehicle tire circumference.
        "vrost": IN,
    },
    "STMDREPE": {
        "ehpe": DE,  # meter error of dr estimated horizontal position
        "reserved1": ST,  #  IN, # reserved fixed as 1.00.
    },
    "STMDRDEBUG": {
        "laterror": DE,  # meter latitude error.
        "lonerror": DE,  # meter longitude error.
        "headingerror": DE,  # degree heading error.
        "speederror": DE,  # m/s speed error.
        "heighterror": DE,  # meter height error.
        "vverror": DE,  # m/s rise speed error.
    },
    "STMDRSENMSG_3": {
        "msgtype": IN,  # 3 = Odometer and Reverse
        "timestamp": IN,  # microsecond cpu tick count since poweron.
        "odometer": DE,
        "reverse": IN,  # 0 = forward, 1 = reverse
    },
    "STMDRSENMSG_24": {
        "msgtype": IN,  # 24 = IMU temperature
        "timestamp": IN,  # microsecond cpu tick count since poweron.
        "temperature": DE,
        "validity": IN,
    },
    "STMDRSENMSG_30": {
        "msgtype": IN,  # 30 = IMU accelerometer
        "timestamp": IN,  # microsecond cpu tick count since poweron.
        "xacc": DE,
        "yacc": DE,
        "zacc": DE,
    },
    "STMDRSENMSG_31": {
        "msgtype": IN,  # 31 = IMU gyroscope
        "timestamp": IN,  # microsecond cpu tick count since poweron.
        "xgyro": DE,
        "ygyro": DE,
        "zgyro": DE,
    },
    "STMDRMMFBKF": {
        "cputime": DE,  # tick
        "elapsedtime": DE,  # tick
        "utcdeltaseconds": DE,  # second
        "utcdeltams": DE,
        "posaccepted": DE,
        "reserved1": ST,
        "reserved2": ST,
        "measurementnoiselat": DE,  # meter
        "posmeasurementnoiselon": DE,  # meter
        "reserved3": ST,
        "reserved4": ST,
        "headingaccepted": DE,
        "reserved5": ST,
        "headingmeasurementnoise": DE,  # degree
        "reserved6": ST,
    },
    # ***************************************************************
    # Septentrio X5 Proprietary message types
    # https://www.septentrio.com/en/products/gnss-receivers/gnss-receiver-modules/mosaic-x5#resources
    # ***************************************************************
    "SSNHRP": {
        "msgId": ST,  # "HRP"
        "utc": TM,
        "date": DT,
        "hdg": DE,  # degrees True
        "roll": DE,
        "pitch": DE,
        "hdgstd": DE,
        "rollstd": DE,
        "pitchstd": DE,
        "sip": IN,
        "attmode": CH,
        "magvar": DE,
        "magvardir": LND,
    },
    "SSNRBD": {
        "msgId": ST,  # "RBD"
        "utc": TM,
        "date": DT,
        "azi": DE,
        "ele": DE,
        "sip": IN,
        "quality": CH,
        "basemode": CH,
        "corrage": DE,
        "roverserial": ST,
        "baseid": ST,
    },
    "SSNRBP": {
        "msgId": ST,  # "RBP"
        "utc": TM,
        "date": DT,
        "baseN": DE,  # meters
        "baseE": DE,
        "baseU": DE,
        "sip": IN,
        "quality": CH,
        "basemode": CH,
        "corrage": DE,
        "roverserial": ST,
        "baseid": ST,
    },
    "SSNRBV": {
        "msgId": ST,  # "RBV"
        "utc": TM,
        "date": DT,
        "baserocN": DE,
        "baserocE": DE,
        "baserocU": DE,
        "sip": IN,
        "quality": CH,
        "basemode": CH,
        "corrage": DE,
        "roverserial": ST,
        "baseid": ST,
    },
    "SSNSNC": {
        "msgId": ST,  # "SNC"
        # "[",
        "rev": CH,
        "tim": IN,  # milliseconds
        "week": IN,
        "group": (
            "None",
            {
                # "[",
                "cdidx": ST,
                "status": QS,
                "errcode": ST,
                "info": ST,
                # "]",
            },
        ),
        # "]",
    },
    "SSNTFM": {
        "msgId": ST,  # "TFM"
        "utc": TM,
        "heightind": ST,
        "usage2122": ST,
        "usage2324": ST,
        "usage252627": ST,
    },
    "STMSETPAROK": {
        "msgId": ST,
        "status1": ST,
        "status2": ST,
        "status3": ST,
    },
    "STMINITGPSERROR": {},
    "STMINITGPSOK": {},
    "STMINITTIMEERROR": {},
    "STMINITTIMEOK": {},
}
