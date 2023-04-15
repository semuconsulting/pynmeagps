"""
NMEA Protocol Output payload definitions

THESE ARE THE PAYLOAD DEFINITIONS FOR _GET_ MESSAGES _FROM_ THE RECEIVER
(e.g. Periodic Navigation Data; Poll Responses; Info messages).

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
    DM,
    HX,
    IN,
    LA,
    LN,
    ST,
    TM,
)

NMEA_PAYLOADS_GET = {
    # *********************************************
    # STANDARD MESSAGES
    # *********************************************
    "AAM": {
        "arrce": CH,
        "perp": CH,
        "crad": DE,
        "cUnit": CH,
        "wpt": ST,
    },
    "APA": {
        "LCgwarn": CH,
        "LCcwarn": CH,
        "ctrkerr": DE,
        "dirs": CH,
        "ctrkUnit": CH,
        "aalmcirc": CH,
        "aalmperp": CH,
        "bearP2D": DE,
        "bearP2Du": CH,
        "wpt": ST,
    },
    "APB": {
        "LCgwarn": CH,
        "LCcwarn": CH,
        "ctrkerr": DE,
        "dirs": CH,
        "ctrkUnit": CH,
        "aalmcirc": CH,
        "aalmperp": CH,
        "bearO2D": DE,
        "bearO2Du": CH,
        "wpt": ST,
        "bearD": DE,
        "bearDu": CH,
        "bearS": DE,
        "bearSu": CH,
    },
    "BOD": {
        "bearT": DE,
        "bearTu": CH,
        "bearM": DE,
        "bearMu": CH,
        "wptD": ST,
        "wptO": ST,
    },
    "BWC": {
        "fixutc": ST,
        "lat": LA,
        "NS": CH,
        "lon": LN,
        "EW": CH,
        "bearT": DE,
        "bearTu": CH,
        "bearM": DE,
        "bearMu": CH,
        "dist": DE,
        "distUnit": CH,
        "wpt": ST,
    },
    "DTM": {
        "datum": ST,
        "subDatum": ST,
        "latOfset": DE,
        "NS": CH,
        "lonOfset": DE,
        "EW": CH,
        "alt": DE,
        "refDatum": ST,
    },
    "GBS": {
        "time": TM,
        "errLat": DE,
        "errLon": DE,
        "errAlt": DE,
        "svid": IN,
        "prob": DE,
        "bias": DE,
        "stddev": DE,
        "systemId": HX,  # NMEA >=4.10 only
        "signalId": HX,  # NMEA >=4.10 only
    },
    "GGA": {
        "time": TM,
        "lat": LA,
        "NS": CH,
        "lon": LN,
        "EW": CH,
        "quality": IN,
        "numSV": IN,
        "HDOP": DE,
        "alt": DE,  # altitude above sea level in m
        "altUnit": CH,
        "sep": DE,
        "sepUnit": CH,
        "diffAge": DE,
        "diffStation": IN,
    },
    "GLL": {
        "lat": LA,
        "NS": CH,
        "lon": LN,
        "EW": CH,
        "time": TM,
        "status": ST,
        "posMode": ST,
    },
    "GMP": {
        "utctime": TM,
        "mapProjection": ST,
        "mapZone": ST,
        "gridN": DE,
        "gridE": DE,
        "modeInd": CH,
        "sip": IN,
        "HDOP": DE,
        "alt": DE,
        "geoidSep": DE,
        "corrAge": DE,
        "baseId": ST,
    },
    "GNS": {
        "time": TM,
        "lat": LA,
        "NS": CH,
        "lon": LN,
        "EW": CH,
        "posMode": ST,
        "numSV": IN,
        "HDOP": DE,
        "alt": DE,
        "sep": DE,
        "diffAge": DE,
        "diffStation": IN,
        "navStatus": CH,  # NMEA >=4.10 only
    },
    "GRS": {
        "time": TM,
        "mode": IN,
        "groupSV": (
            12,
            {  # repeating group * 12
                "residual": DE,
            },
        ),
        "systemId": HX,  # NMEA >=4.10 only
        "signalId": HX,  # NMEA >=4.10 only
    },
    "GSA": {
        "opMode": CH,
        "navMode": IN,
        "groupSV": (
            12,
            {  # repeating group * 12
                "svid": IN,
            },
        ),
        "PDOP": DE,
        "HDOP": DE,
        "VDOP": DE,
        "systemId": HX,  # NMEA >=4.10 only
    },
    "GST": {
        "time": TM,
        "rangeRms": DE,
        "stdMajor": DE,
        "stdMinor": DE,
        "orient": DE,
        "stdLat": DE,
        "stdLong": DE,
        "stdAlt": DE,
    },
    "GSV": {
        "numMsg": IN,
        "msgNum": IN,
        "numSV": IN,
        "group_sv": (
            "None",
            {  # repeating group * 1..4
                "svid": IN,
                "elv": DE,  # elevation
                "az": IN,  # azimuth
                "cno": IN,  # signal strength
            },
        ),
        "signalID": HX,  # NMEA >=4.10 only
    },
    "HDG": {
        "heading": DE,
        "MT": CH,  # 'M'
    },
    "HDM": {
        "heading": DE,
        "devm": DE,
        "devEW": CH,
        "varm": DE,
        "varEW": CH,
    },
    "HDT": {
        "heading": DE,
        "MT": CH,  # 'T'
    },
    "LLQ": {
        "utctime": TM,
        "utcdate": DT,
        "easting": DE,
        "eunit": CH,  # 'M'
        "northing": DE,
        "nunit": CH,  # 'M'
        "gpsQual": IN,
        "sip": IN,
        "posQual": DE,
        "height": DE,
        "hunit": CH,  # 'M'
    },
    "MSK": {
        "freq": DE,
        "fmode": CH,
        "beacbps": IN,
        "bpsmode": CH,
        "MMSfreq": DE,
    },
    "MSS": {
        "strength": IN,
        "snr": IN,
        "freq": DE,
        "beacbps": IN,
    },
    "ROT": {
        "rot": DE,  # -ve = turn to port
        "valid": CH,  # A valid, V invalid
    },
    "RLM": {
        "beacon": HX,
        "time": TM,
        "code": CH,
        "body": HX,
    },
    "RMA": {
        "status": CH,
        "lat": LA,
        "NS": CH,
        "lon": LN,
        "EW": CH,
        "reserved1": ST,
        "reserved2": ST,
        "sog": DE,
        "cog": DE,
        "var": DE,
        "dirvar": CH,
    },
    "RMB": {
        "status": CH,
        "ctrkerr": DE,
        "dirs": CH,
        "wptO": CH,
        "wptD": CH,
        "lat": LA,  # of wptD
        "NS": CH,
        "lon": LN,  # of wptD
        "EW": CH,
        "range": DE,
        "bearing": DE,
        "velclos": DE,
        "arrstatus": CH,
        "valstatus": CH,
    },
    "RMC": {
        "time": TM,
        "status": CH,
        "lat": LA,
        "NS": CH,
        "lon": LN,
        "EW": CH,
        "spd": DE,  # speed in knots
        "cog": DE,  # course over ground
        "date": DT,
        "mv": DE,
        "mvEW": ST,
        "posMode": CH,
        "navStatus": CH,  # NMEA >=4.10 only
    },
    "RTE": {
        "numMsg": IN,
        "msgNum": IN,
        "status": CH,  # 'c'/'w'
        "active": ST,
        "group_wp": (
            "None",
            {  # repeating group
                "wpt": ST,
            },
        ),
    },
    "STN": {
        "talkerId": ST,
    },
    "THS": {
        "headt": DE,
        "mi": CH,
    },
    "TRF": {
        "time": TM,
        "date": DT,
        "lat": LA,
        "NS": CH,
        "lon": LN,
        "EW": CH,
        "elangle": DE,
        "iter": DE,
        "Dopint": DE,
        "dist": DE,
        "svid": IN,
    },
    "TXT": {
        "numMsg": IN,
        "msgNum": IN,
        "msgType": IN,
        "text": ST,
    },
    "VBW": {
        "wlspd": DE,
        "wtspd": DE,
        "wstatus": CH,
        "glspd": DE,
        "gtspd": DE,
        "gstatus": CH,
    },
    "VLW": {
        "twd": DE,
        "twdUnit": CH,
        "wd": DE,
        "wdUnit": CH,
        "tgd": DE,  # NMEA >=4.00 only
        "tgdUnit": CH,  # NMEA >=4.00 only
        "gd": DE,  # NMEA >=4.00 only
        "gdUnit": CH,  # NMEA >=4.00 only
    },
    "VTG": {
        "cogt": DE,  # course over ground (true)
        "cogtUnit": CH,
        "cogm": DE,  # course over ground (magnetic)
        "cogmUnit": CH,
        "sogn": DE,  # speed over ground knots
        "sognUnit": CH,
        "sogk": DE,  # speed over ground kmph
        "sogkUnit": CH,
        "posMode": CH,  # NMEA >=2.3 only
    },
    "WPL": {
        "lat": LA,
        "NS": CH,
        "lon": LN,
        "EW": CH,
        "wpt": ST,
    },
    "XTE": {
        "gwarn": CH,
        "LCcwarn": CH,
        "ctrkerr": DE,
        "dirs": CH,
        "disUnit": CH,
    },
    "ZDA": {
        "time": TM,
        "day": IN,
        "month": IN,
        "year": IN,
        "ltzh": ST,
        "ltzn": ST,
    },
    # *********************************************
    # JVCKENWOOD PROPRIETARY MESSAGES
    # *********************************************
    "KLSH": {
        "lat": LA,
        "NS": CH,
        "lon": LN,
        "EW": CH,
        "time": TM,
        "status": CH,
        "fleetId": ST,
        "deviceId": ST,
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
        "NS": CH,
        "lon": LN,
        "EW": CH,
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
        "NS": CH,
        "lon": LN,
        "EW": CH,
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
        "NS": CH,
        "lon": LN,
        "EW": CH,
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
    "ASHRHR": {
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
        "NS": CH,
        "lon": LN,
        "EW": CH,
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
        "NS": CH,
        "lon": LN,
        "EW": CH,
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
        "NS": CH,
        "lon": LN,
        "EW": CH,
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
        "NS": CH,
        "lon": LN,
        "EW": CH,
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
        "NS": CH,
        "lon": LN,
        "EW": CH,
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
        "NS": CH,
        "lon": LN,
        "EW": CH,
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
    # Dummy message for error testing
    # *********************************************
    "FOO": {"spam": "Z2", "eggs": "Y1"},
}
