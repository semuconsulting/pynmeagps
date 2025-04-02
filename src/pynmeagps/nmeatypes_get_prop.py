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

:author: semuadmin
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
    "QTMCFGCNST": {
        "status": QS,
        "gps": IN,
        "glonass": IN,
        "galileo": IN,
        "beidou": IN,
        "qzss": IN,
        "navic": IN,
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
    "QTMCFGNMEADP": {
        "status": QS,
        "utcdp": IN,
        "posdp": IN,
        "altdp": IN,
        "dopdp": IN,
        "spddp": IN,
        "cogdp": IN,
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
        "msmelevthd": IN,
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
    "QTMCFGSIGNAL": {
        "status": QS,
        "gpssig": ST,  # hex as string, default 07
        "glonasssig": ST,  # hex as string, default 03
        "galileosig": ST,  # hex as string, default 0F
        "beidousig": ST,  # hex as string, default 3F
        "qzsssig": ST,  # hex as string, default 07
        "navicsig": ST,  # hex as string, default 01
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
    "QTMDEBUGON": {"status": ST},
    "QTMDEBUGOFF": {"status": ST},
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
    "QTMEPE": {
        "msgver": IN,  # always 2 for this version
        "epenorth": DE,
        "epeeast": DE,
        "epedown": DE,
        "epe2d": DE,
        "epe3d": DE,
    },
    "QTMGEOFENCESTATUS": {"msgver": IN, "time": TM, "group": (4, {"staten": IN})},
    "QTMGNSSSTART": {"status": ST},
    "QTMGNSSSTOP": {"status": ST},
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
    "QTMRESETODO": {"status": ST},
    "QTMRESTOREPAR": {"status": ST},
    "QTMSAVEPAR": {"status": ST},
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
}
