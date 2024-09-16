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
    DM,
    DT,
    DTL,
    HX,
    IN,
    LA,
    LAD,
    LN,
    LND,
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
        "cUnit": CH,  # N nm
        "wpt": ST,
    },
    "ABK": {
        "mmsi": ST,
        "aischan": CH,
        "itumsg": ST,
        "msgSeq": IN,
        "ackType": IN,
    },
    "ABM": {
        "numSen": IN,
        "senNum": IN,
        "mmsi": ST,
        "aischan": CH,
        "ituMsg": ST,
        "data": ST,
        "fillbits": IN,
    },
    "ACA": {
        "seqNum": IN,
        "latne": LA,
        "latneNS": LAD,
        "lonne": LN,
        "lonneEW": LND,
        "latsw": LA,
        "latswNS": LAD,
        "lonswq": LN,
        "lonswEW": LND,
        "tranZoneSize": CH,
        "chanA": CH,
        "chanAbw": CH,
        "chanB": CH,
        "chanBbw": CH,
        "txrxMode": IN,
        "pwrLevelCtl": IN,
        "infoSource": CH,
        "inuse": IN,
        "inuseTime": TM,
    },
    "ACK": {
        "alarmid": ST,
    },
    "ACN": {
        "time": TM,
        "mfrcode": ST,
        "alertid": ST,
        "alertnum": IN,
        "alertcmd": ST,
        "status": CH,
    },
    "ACS": {
        "seqNum": IN,
        "mmsi": ST,
        "utc": TM,
        "day": IN,
        "month": IN,
        "year": IN,
    },
    "AIR": {
        "mmsi1": ST,
        "mmsi1msg1": ST,
        "mmsi1msg1sub": ST,
        "mmsi1msg2": ST,
        "mmsi1msg2sub": CH,
        "mmsi2": ST,
        "mmsi2msg1": ST,
        "mmsi2msg1sub": ST,
        "channel": ST,
        "mid11": ST,
        "mid12": ST,
        "mid21": ST,
    },
    "AKD": {
        "acktime": TM,
        "srcsystem": ST,
        "srcsubsysytem": ST,
        "srcinstance": ST,
        "alarmtype": ST,
        "acksystem": ST,
        "acksubsystem": ST,
        "ackinstance": ST,
    },
    "ALA": {
        "evttime": TM,
        "srcsystem": ST,
        "srcsubsysytem": ST,
        "srcinstance": ST,
        "alarmtype": ST,
        "alarmcond": ST,
        "alarmackstate": ST,
        "alarmtext": ST,
    },
    "ALC": {
        "numSen": IN,
        "senNum": IN,
        "seqmid": IN,
        "numAlerts": IN,
        "alertgroup": (  # repeating group * numAlerts
            "numAlerts",
            {
                "mfrcode": ST,
                "alertid": ST,
                "revisionctr": ST,
            },
        ),
    },
    "ALF": {
        "numSen": IN,
        "senNum": IN,
        "seqmid": IN,
        "timelastchange": TM,
        "alertcat": CH,  # A, B, C
        "alertpriority": CH,  # E, A W, C
        "alertstate": CH,  # A, S, N, O, U, V
        "mfrcode": ST,
        "alertid": ST,
        "alertinst": ST,
        "revisionctr": ST,
        "escalationctr": ST,
        "alerttxt": ST,  # max 16 chars
    },
    "ALR": {
        "timealarmchange": TM,
        "alarmnum": ST,
        "alarmcond": ST,
        "alarmstate": ST,
        "alarmtext": ST,
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
        "mode": CH,
    },
    "ARC": {
        "time": TM,
        "mfrcode": ST,
        "alertid": ST,
        "alertinst": IN,
        "alertcmd": ST,
    },
    "BBM": {
        "numSen": IN,
        "senNum": IN,
        "seqmid": IN,
        "aischan": CH,
        "itumsg": ST,
        "data": ST,
        "fillbits": IN,
    },
    "BEC": {
        "utc": TM,
        "wptlat": LA,
        "wptNS": LAD,
        "wptlon": LN,
        "wptEW": LND,
        "bearT": DE,
        "bearTu": CH,  # 'T'rue
        "bearM": DE,
        "bearMu": CH,  # 'M'agnetic
        "dist": DE,
        "distu": CH,  # 'N'autical Miles
        "wpt": ST,
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
        "fixutc": TM,
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "bearT": DE,
        "bearTu": CH,  # 'T'
        "bearM": DE,
        "bearMu": CH,  # 'M'
        "dist": DE,
        "distUnit": CH,  # 'N'
        "wpt": ST,
        "mode": CH,
    },
    "BWR": {
        "fixutc": TM,
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "bearT": DE,
        "bearTu": CH,  # 'T'
        "bearM": DE,
        "bearMu": CH,  # 'M'
        "dist": DE,
        "distUnit": CH,  # 'N'
        "wpt": ST,
        "mode": CH,
    },
    "BWW": {
        "bearT": DE,
        "bearTu": CH,  # 'T'
        "bearM": DE,
        "bearMu": CH,  # 'M'
        "wptto": ST,
        "wptfrom": ST,
    },
    "CUR": {
        "valid": CH,
        "datasetnum": IN,
        "layernum": IN,
        "depth": DE,
        "direction": DE,
        "dirTR": CH,  # 'T' or 'R'
        "speed": DE,
        "refdepth": DE,
        "heading": DE,
        "headingTM": CH,  # 'T' or 'M'
        "speedref": CH,  # 'B', 'W', 'P'
    },
    "DBT": {
        "depthf": DE,
        "depthfu": CH,  # 'f'eet
        "depthm": DE,
        "depthmu": CH,  # 'M'eter
        "depthfath": DE,
        "depthfathu": CH,  # 'F'athoms
    },
    "DDC": {
        "preset": CH,
        "brightness": IN,
        "palette": CH,
        "status": CH,
    },
    "DOR": {
        "msgtype": CH,
        "time": TM,
        "doormontype": ST,
        "div1ind": ST,
        "div2ind": ST,
        "doorcount": IN,
        "doorstatus": CH,
        "watertightdoorsetting": CH,
        "msgtext": ST,
    },
    "DPT": {
        "depth": DE,  # m
        "offset": DE,
        "rangescale": DE,
    },
    "DSC": {
        "format": ST,
        "address": ST,
        "category": ST,
        "distresstype": ST,
        "commtype": ST,
        "channel": ST,
        "timetelno": ST,
        "mmsi": ST,
        "distressnature": ST,
        "acknowledgement": CH,
        "expansionind": CH,
    },
    "DSE": {
        "numSen": IN,
        "senNum": IN,
        "queryflag": CH,
        "mmsi": ST,
        "datagroup": (
            "None",  # variable repeating group
            {
                "code": ST,
                "data": ST,
            },
        ),
    },
    "DTM": {
        "datum": ST,
        "subDatum": ST,
        "latOfset": DE,
        "NS": LAD,
        "lonOfset": DE,
        "EW": LND,
        "alt": DE,
        "refDatum": ST,
    },
    "EPV": {
        "status": CH,
        "equipmenttype": ST,
        "equipmentid": ST,
        "propertyid": ST,
        "value": ST,
    },
    "ETL": {
        "time": TM,
        "msgtype": CH,
        "engtelposind": ST,
        "engsubtelposind": ST,
        "operatinglocind": CH,
        "enginenum": CH,
    },
    "EVE": {
        "time": TM,
        "tagcode": ST,
        "eventtext": ST,
    },
    "FIR": {
        "msgtype": CH,
        "time": TM,
        "fdstype": ST,
        "div1ind": ST,
        "div2ind": ST,
        "fdsnum": ST,
        "condition": CH,
        "alarmackstate": CH,
        "text": ST,
    },
    "FSI": {
        "txfreq": ST,
        "rxfreq": ST,
        "opmode": ST,
        "power": IN,
        "status": CH,
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
    "GEN": {
        "index": HX,
        "time": TM,
        "group": ("None", {"data": HX}),  # variable repeating group
    },
    "GFA": {
        "time": TM,
        "hprotlvl": DE,
        "vprotlvl": DE,
        "semimajstddev": DE,
        "semiminstddev": DE,
        "semimajorientation": DE,
        "altstddev": DE,
        "accuracy": DE,
        "integrity": ST,  # V not in use, 'S'afe, 'C'aution, 'U'nsafe
    },
    "GGA": {
        "time": TM,
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
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
        "NS": LAD,
        "lon": LN,
        "EW": LND,
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
        "NS": LAD,
        "lon": LN,
        "EW": LND,
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
    "HBT": {
        "repeatint": DE,
        "status": CH,
        "seqid": IN,
    },
    "HCR": {
        "headingt": DE,
        "mode": CH,
        "corrstate": CH,
        "corrvalue": DE,
    },
    "HDG": {
        "headingM": DE,
        "deviation": DE,
        "deviationEW": LND,
        "variation": DE,
        "variationEW": LND,
    },
    "HDM": {
        "headingM": DE,
        "deviation": DE,
        "deviationEW": LND,
        "variation": DE,
        "variationEW": LND,
    },
    "HDT": {
        "headingT": DE,
        "headingTu": CH,  # 'T'
    },
    "HMR": {
        "sensor1id": ST,
        "sensor2id": ST,
        "setdiff": DE,
        "actualdiff": DE,
        "warning": CH,  # A within set, V exceeds set
        "sensor1hdg": DE,
        "sensor1status": CH,
        "sensor1u": CH,  # 'T'rue, 'M'agnetic
        "sensor1dev": DE,
        "sensor1EW": LND,
        "sensor2hdg": DE,
        "sensor2status": CH,
        "sensor2u": CH,  # 'T'rue, 'M'agnetic
        "sensor2dev": DE,
        "sensor2EW": LND,
        "variation": DE,
        "variationEW": LND,
    },
    "HMS": {
        "sensor1id": ST,
        "sensor2id": ST,
        "setdiff": DE,
    },
    "HRM": {
        "heel": DE,
        "rollperiod": DE,
        "rollamplitudeport": DE,
        "rollamplitduestbd": DE,
        "status": CH,
        "rollpeakport": DE,
        "rollpeakstbd": DE,
        "peakholdresettime": TM,
        "peakholdresetdat": IN,
        "peakholdresetmonth": IN,
    },
    "HSC": {
        "cmdheadingT": DE,
        "cmdheadingTu": CH,  # 'T'
        "cmdheadingM": DE,
        "cmdheadingMu": CH,  # 'M'
        "status": CH,
    },
    "HSS": {
        "measpointid": ST,
        "value": DE,
        "status": CH,
    },
    "HTC": {
        "override": CH,  # A in use V not in use
        "cmdrudderang": DE,
        "cmdrudderdir": CH,  # L port R stbd
        "steermode": CH,
        "turnmode": CH,  # 'R'adius, 'T'urn rate, 'N'ot controlled
        "cmdrudderlimit": DE,
        "cmdoffheadinglimit": DE,
        "cmdturnradius": DE,
        "cmdturnrate": DE,
        "cmdheading": DE,
        "cmdofftracklimit": DE,
        "cmdtrack": DE,
        "headingref": CH,  # 'T'rue, 'M'agnetic
        "status": CH,
    },
    "HTD": {
        "override": CH,  # A in use V not in use
        "cmdrudderang": DE,
        "cmdrudderdir": CH,  # L port R stbd
        "steermode": CH,
        "turnmode": CH,  # 'R'adius, 'T'urn rate, 'N'ot controlled
        "cmdrudderlimit": DE,
        "cmdoffheadinglimit": DE,
        "cmdturnradius": DE,
        "cmdturnrate": DE,
        "cmdheading": DE,
        "cmdofftracklimit": DE,
        "cmdtrack": DE,
        "headingref": CH,  # 'T'rue, 'M'agnetic
        "rudderstatus": CH,
        "offheadingstatus": CH,
        "offtrackstatus": CH,
        "vesselheading": DE,
    },
    "LR1": {
        "seqNum": IN,
        "mmsiresponder": ST,
        "mmsirequester": ST,
        "shipname": ST,
        "callsign": ST,
        "imonum": ST,
    },
    "LR2": {
        "seqNum": IN,
        "mmsiresponder": ST,
        "date": DTL,
        "time": TM,
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "cog": DE,  # course over ground
        "cogT": CH,  # 'T'
        "sog": DE,  # speed over ground
        "sogu": CH,  # 'N' knots
    },
    "LR3": {
        "seqNum": IN,
        "mmsiresponder": ST,
        "destination": ST,
        "etadate": DT,
        "etatime": TM,
        "draught": DE,
        "cargo": DE,
        "length": DE,
        "breadth": DE,
        "type": DE,
        "persons": DE,
    },
    "LRF": {
        "seqNum": IN,
        "mmsirequestor": ST,
        "namerequestor": ST,
        "function": ST,
        "replystatus": ST,
    },
    "LRI": {
        "seqNum": IN,
        "controlflag": CH,
        "mmsirequestor": ST,
        "mmsidestination": ST,
        "latne": LA,
        "NSne": LAD,
        "lonne": LN,
        "EWne": LND,
        "latsw": LA,
        "NSsw": LAD,
        "lonsw": LN,
        "EWsw": LND,
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
    "MOB": {
        "emitterid": ST,
        "mobstatus": CH,
        "timeactivation": TM,
        "mobpossource": CH,
        "dayactivated": IN,
        "timeposition": TM,
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "cog": DE,  # true
        "sog": DE,  # knots
        "mmsi": ST,
        "batterystatus": CH,
    },
    "MSK": {
        "freq": DE,
        "fmode": CH,  # 'A'uto, 'M'anual
        "beacbps": IN,
        "bpsmode": CH,  # 'A'uto, 'M'anual
        "MMSfreq": DE,
        "channel": CH,
        "status": CH,
    },
    "MSS": {
        "strength": IN,
        "snr": IN,
        "freq": DE,
        "beacbps": IN,
        "channel": CH,
    },
    "MTW": {
        "temp": DE,
        "tempu": CH,  # degrees C
    },
    "MWD": {
        "dirT": DE,
        "dirTu": CH,  # 'T'rue
        "dirM": DE,
        "dirMu": CH,  # 'M'agnetic
        "speedN": DE,
        "speedNu": CH,  # 'N' knots
        "speedM": DE,
        "speedMu": CH,  # 'M' m/s
    },
    "MWV": {
        "angle": DE,
        "reference": CH,  # 'R'elative, 'T'heoretical
        "speed": DE,
        "speedu": CH,  # K km/h, M m/s N knots
        "status": CH,
    },
    "NAK": {
        "talker": ST,
        "formatter": ST,
        "identifier": ST,
        "reason": ST,
        "text": ST,
    },
    "NRM": {
        "function": CH,
        "freqtable": CH,
        "txcovermask": HX,
        "msgtypemask": HX,
        "status": CH,
    },
    "NRX": {
        "numSen": IN,
        "senNum": IN,
        "seqid": IN,
        "msgcode": CH,
        "freqtable": CH,
        "time": TM,
        "day": IN,
        "month": IN,
        "year": IN,
        "totalchar": DE,
        "totalbad": DE,
        "status": CH,
        "body": ST,
    },
    "NSR": {
        "hdgintegrity": CH,
        "hdgplausibility": CH,
        "posintegrity": CH,
        "posplausibility": CH,
        "stwintegrity": CH,
        "stwplausibility": CH,
        "sogcogintegrity": CH,
        "sogcogplausibility": CH,
        "depthintegrity": CH,
        "depthplausibility": CH,
        "stwmode": CH,
        "timeintegrity": CH,
        "timeplausibility": CH,
    },
    "OSD": {
        "hdg": DE,
        "hdgstate": CH,
        "course": DE,
        "courseref": CH,
        "speed": DE,
        "speedref": CH,
        "set": DE,
        "drift": DE,
        "speedu": CH,  # K km/h N knots S mph
    },
    "POS": {
        "equipmentid": ST,
        "equipmentnum": IN,
        "posvalidity": CH,
        "posx": DE,
        "posy": DE,
        "posz": DE,
        "shipdimvalid": CH,
        "width": DE,
        "length": DE,
        "status": CH,
    },
    "PRC": {
        "leverdmdpos": DE,
        "leverdmdstatus": CH,
        "rpmdemand": DE,
        "rpmdemandstatus": CH,
        "pitchdmd": DE,
        "pitchmode": CH,
        "operatinglocind": CH,
        "engineshaftnum": IN,
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
        "NS": LAD,
        "lon": LN,
        "EW": LND,
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
        "NS": LAD,
        "lon": LN,  # of wptD
        "EW": LND,
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
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "spd": DE,  # speed in knots
        "cog": DE,  # course over ground
        "date": DT,
        "mv": DE,
        "mvEW": ST,
        "posMode": CH,
        "navStatus": CH,  # NMEA >=4.10 only
    },
    "ROR": {
        "stbdrudderorder": DE,
        "stbdrudderstatus": CH,
        "portrudderorder": DE,
        "portrudderstatus": CH,
        "operatinglocind": CH,
    },
    "ROT": {
        "rot": DE,  # -ve = turn to port
        "valid": CH,  # A valid, V invalid
    },
    "RRT": {
        "tfrtype": CH,
        "tfrroutename": ST,
        "tfrroutever": ST,
        "wptid": ST,
        "filestatus": CH,
        "appstatus": CH,
    },
    "RPM": {
        "source": CH,
        "engineshaftnum": IN,
        "rpm": DE,
        "pitch": DE,
        "status": CH,
    },
    "RSA": {
        "stbdangle": DE,
        "stbdstatus": CH,
        "portangle": DE,
        "portstatus": CH,
    },
    "RSD": {
        "origin1range": DE,
        "origin1bearing": DE,
        "vrm1": DE,
        "ebl1": DE,
        "origin2range": DE,
        "origin2bearing": DE,
        "vrm2": DE,
        "ebl2": DE,
        "cursorrange": DE,
        "rangebearing": DE,
        "rangescale": DE,
        "rangeu": CH,  # K kn N nautical mile S statute mile
        "displayrot": CH,
    },
    "RTE": {
        "numMsg": IN,
        "msgNum": IN,
        "status": CH,  # 'c'/'w'
        "routeid": ST,
        "group_wp": (
            "None",
            {  # repeating group
                "wpt": ST,
            },
        ),
    },
    "SFI": {
        "numSen": IN,
        "senNum": IN,
        "freqgroup": (
            6,  # repeating group * 6
            {
                "freq": IN,
                "mode": ST,
            },
        ),
    },
    "SM1": {
        "MSIstatus": CH,
        "msgnum": IN,
        "LESseqnum": IN,
        "LESid": IN,
        "oceanregioncode": IN,
        "prioritycode": IN,
        "servicecode": IN,
        "presentationcode": IN,
        "year": IN,
        "month": IN,
        "day": IN,
        "hour": IN,
        "minute": IN,
        "addresscode": IN,
    },
    "SM2": {
        "MSIstatus": CH,
        "msgnum": IN,
        "LESseqnum": IN,
        "LESid": IN,
        "oceanregioncode": IN,
        "prioritycode": IN,
        "servicecode": IN,
        "presentationcode": IN,
        "year": IN,
        "month": IN,
        "day": IN,
        "hour": IN,
        "minute": IN,
        "coastalwarnnavarea": IN,
        "coastalwarnnavarea": CH,
        "coastalwarnsubjectind": CH,
    },
    "SM3": {
        "MSIstatus": CH,
        "msgnum": IN,
        "LESseqnum": IN,
        "LESid": IN,
        "oceanregioncode": IN,
        "prioritycode": IN,
        "servicecode": IN,
        "presentationcode": IN,
        "year": IN,
        "month": IN,
        "day": IN,
        "hour": IN,
        "minute": IN,
        "circarealat": LA,
        "circareaNS": LAD,
        "circarealon": LN,
        "circareaEW": LND,
        "circarearadius": IN,
    },
    "SM4": {
        "MSIstatus": CH,
        "msgnum": IN,
        "LESseqnum": IN,
        "LESid": IN,
        "oceanregioncode": IN,
        "prioritycode": IN,
        "servicecode": IN,
        "presentationcode": IN,
        "year": IN,
        "month": IN,
        "day": IN,
        "hour": IN,
        "minute": IN,
        "redareaswlat": LA,
        "recareaswNS": LAD,
        "redareaswlon": LN,
        "recareaswEW": LND,
        "recareaextentN": IN,
        "recareaextentE": IN,
    },
    "SMB": {"numSen": IN, "senNum": IN, "seqid": IN, "msgnum": IN, "body": ST},
    "SPW": {
        "pwdprotectsentence": ST,
        "id": ST,
        "pwdlevel": IN,
        "password": ST,
    },
    "SSD": {
        "callsign": ST,
        "name": ST,
        "posAref": IN,  # bow
        "posBref": IN,  # stern
        "posCref": IN,  # port beam
        "posDref": IN,  # stbd beam
        "DTEind": ST,
        "sourceid": ST,
    },
    "STN": {
        "talkerId": ST,
    },
    "THS": {
        "headt": DE,
        "mi": CH,
    },
    "TLB": {
        "group": (
            "None",  # indeterminate repeating group
            {
                "targetnum": IN,
                "label": ST,
            },
        )
    },
    "TLL": {
        "targetnum": IN,
        "targetlat": LA,
        "targetlatNS": LAD,
        "targetlon": LN,
        "targetlonEW": LND,
        "targetname": ST,
        "time": TM,
        "status": CH,
        "reftarget": CH,
    },
    "TRC": {
        "thrusternum": IN,
        "dmdrpm": DE,
        "rpmmode": CH,
        "dmdpitch": DE,
        "pitchmode": CH,
        "dmdazimuth": DE,
        "operatinglocind": CH,
        "status": CH,
    },
    "TRD": {
        "thrusternum": IN,
        "rpmresponse": IN,
        "rpmmode": CH,
        "pitchresponse": IN,
        "pitchmode": CH,
        "azimuthresponse": IN,
    },
    "TRL": {
        "totlognum": IN,
        "lognum": IN,
        "seqid": IN,
        "switchoffdate": ST,
        "switchofftime": TM,
        "switchondate": ST,
        "switchontime": TM,
        "reasoncode": IN,
    },
    "TRF": {
        "time": TM,
        "date": DT,
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "elangle": DE,
        "iter": DE,
        "Dopint": DE,
        "dist": DE,
        "svid": IN,
    },
    "TTD": {
        "numSen": IN,
        "senNum": IN,
        "seqid": IN,
        "data": ST,
        "fillbits": IN,
    },
    "TTM": {
        "targetnum": IN,
        "targetdist": DE,
        "targetbearing": DE,
        "targetbearingu": CH,  # 'T'rue, 'R'relative
        "targetspeed": DE,
        "targetcourse": DE,
        "targetcourseu": CH,  # 'T'rue, 'R'relative
        "closestapproach": DE,
        "timetoCPA": DE,
        "speedu": CH,
        "targetname": ST,
        "targetstatus": CH,
        "reftarget": ST,
        "time": TM,
        "acquisitiontype": CH,
    },
    "TUT": {
        "sourceid": ST,
        "numSen": HX,
        "senNum": HX,
        "seqid": IN,
        "translationcode": ST,
        "text": ST,
    },
    "TXT": {
        "numMsg": IN,
        "msgNum": IN,
        "msgType": IN,
        "text": ST,
    },
    "UID": {
        "uid1": ST,
        "uid2": ST,  # optional
    },
    "VBW": {
        "longwaterspd": DE,  # -ve = astern
        "transwaterspd": DE,
        "waterspdstatus": CH,
        "longgroundspd": DE,  # -ve = astern
        "transgroundspd": DE,  # -ve = port
        "groundspdstatus": CH,
        "sterntranswaterspd": DE,  # -ve = port
        "sternwaterspdstatus": CH,
        "sterntransgroundspd": DE,  # -ve = port
        "sterngroundspdstatus": CH,
    },
    "VDM": {
        "numSen": IN,
        "senNum": IN,
        "seqid": IN,
        "aischan": ST,
        "itumsg": ST,
        "fillbits": IN,
    },
    "VDO": {
        "numSen": IN,
        "senNum": IN,
        "seqid": IN,
        "aischan": ST,
        "itumsg": ST,
        "fillbits": IN,
    },
    "VDR": {
        "dirT": DE,
        "dirTu": CH,  # 'T'rue
        "dirM": DE,
        "dirMu": CH,  # 'M'agnetic
        "spd": DE,
        "spdu": CH,  # N knots
    },
    "VER": {
        "numSen": IN,
        "senNum": IN,
        "devicetype": ST,
        "vendorid": ST,
        "uid": ST,
        "mfrserial": ST,
        "model": ST,
        "software": ST,
        "hardware": ST,
        "seqid": IN,
    },
    "VHW": {
        "hdgT": DE,
        "hgdTu": CH,  # 'T'rue
        "hdgM": DE,
        "hgdMu": CH,  # 'M'agnetic
        "spdN": DE,
        "spdNu": CH,  # N knots
        "spdK": DE,
        "spdKu": CH,  # K km/h
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
    "VPW": {
        "spdN": DE,
        "spdNu": CH,  # N knots
        "spdK": DE,
        "spdKu": CH,  # K km/h
    },
    "VSD": {
        "type": ST,
        "draught": DE,
        "pob": IN,
        "destination": ST,
        "etatime": TM,
        "etaday": IN,
        "etamonth": IN,
        "regappflags1": IN,
        "regappflags2": IN,
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
    "WAT": {
        "msgtype": CH,
        "time": TM,
        "alarmtype": ST,
        "loc1ind": IN,
        "loc2ind": IN,
        "detectionpoint": IN,
        "alarmcondition": CH,
        "overridesetting": CH,
        "text": ST,
    },
    "WCV": {
        "vel": DE,
        "velu": CH,  # N knots
        "wpt": ST,
        "mode": CH,
    },
    "WNC": {
        "distN": DE,
        "distNu": CH,  # 'N' nm
        "distK": DE,
        "distKu": CH,  # 'K' km
        "wptto": ST,
        "wptfrom": ST,
    },
    "WPL": {
        "lat": LA,
        "NS": LAD,
        "lon": LN,
        "EW": LND,
        "wpt": ST,
    },
    "XDR": {
        "group": (
            "None",  # indeterminate repeating group
            {
                "tdrtype": CH,
                "data": DE,
                "dataunit": CH,
                "tdrid": ST,
            },
        )
    },
    "XTE": {
        "gwarn": CH,
        "LCcwarn": CH,
        "ctrkerr": DE,
        "dirs": CH,
        "disUnit": CH,  # N nm
        "mode": CH,
    },
    "XTR": {
        "ctkerr": DE,
        "steerdir": CH,
        "units": CH,  # N nm
    },
    "ZDA": {
        "time": TM,
        "day": IN,
        "month": IN,
        "year": IN,
        "ltzh": ST,
        "ltzn": ST,
    },
    "ZDL": {
        "time": TM,
        "dist": DE,
        "type": CH,
    },
    "ZFO": {
        "observationtime": TM,
        "elapsedtime": TM,
        "originwpt": ST,
    },
    "ZTG": {
        "observationtime": TM,
        "timetogo": TM,
        "destwpt": ST,
    },
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
    # *********************************************
    # Dummy message for error testing
    # *********************************************
    "FOO": {"spam": "Z2", "eggs": "Y1"},
}
