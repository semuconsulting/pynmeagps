"""
NMEA Protocol Output (GET) payload definitions

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

# pylint: disable=too-many-lines, duplicate-code

from pynmeagps.nmeatypes_core import CH, DE, DT, DTL, HX, IN, LA, LAD, LN, LND, ST, TM

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
        "talkerid": ST,
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
        "coastalwarnarea": CH,
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
    # Dummy message for error testing
    # *********************************************
    "FOO": {"spam": "Z2", "eggs": "Y1"},
}
