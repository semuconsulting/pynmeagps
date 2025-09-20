"""
Collection of NMEA helper methods which can be used
outside the NMEAMessage or NMEAReader classes

Created on 04 Mar 2021

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2021
:license: BSD 3-Clause
"""

# pylint: disable=invalid-name

import re
from datetime import datetime
from math import acos, asin, atan2, cos, pi, sin, sqrt

import pynmeagps.exceptions as nme
from pynmeagps.nmeatypes_core import (
    DM,
    DT,
    DTL,
    GPSEPOCH0,
    LA,
    LN,
    NMEA_MSGIDS,
    NMEA_MSGIDS_PROP,
    WGS84,
    WGS84_FLATTENING,
    WGS84_SMAJ_AXIS,
)

KNOTSCONV = {"MS": 0.5144447324, "FS": 1.68781084, "MPH": 1.15078, "KMPH": 1.852001}
LEAPS0 = datetime(1900, 1, 1, 0, 0, 0)
LEAPSECONDS = [
    (2272060800, 10),  # 1 Jan 1972
    (2287785600, 11),  # 1 Jul 1972
    (2303683200, 12),  # 1 Jan 1973
    (2335219200, 13),  # 1 Jan 1974
    (2366755200, 14),  # 1 Jan 1975
    (2398291200, 15),  # 1 Jan 1976
    (2429913600, 16),  # 1 Jan 1977
    (2461449600, 17),  # 1 Jan 1978
    (2492985600, 18),  # 1 Jan 1979
    (2524521600, 19),  # 1 Jan 1980
    (2571782400, 20),  # 1 Jul 1981
    (2603318400, 21),  # 1 Jul 1982
    (2634854400, 22),  # 1 Jul 1983
    (2698012800, 23),  # 1 Jul 1985
    (2776982400, 24),  # 1 Jan 1988
    (2840140800, 25),  # 1 Jan 1990
    (2871676800, 26),  # 1 Jan 1991
    (2918937600, 27),  # 1 Jul 1992
    (2950473600, 28),  # 1 Jul 1993
    (2982009600, 29),  # 1 Jul 1994
    (3029443200, 30),  # 1 Jan 1996
    (3076704000, 31),  # 1 Jul 1997
    (3124137600, 32),  # 1 Jan 1999
    (3345062400, 33),  # 1 Jan 2006
    (3439756800, 34),  # 1 Jan 2009
    (3550089600, 35),  # 1 Jul 2012
    (3644697600, 36),  # 1 Jul 2015
    (3692217600, 37),  # 1 Jan 2017
]
"""
Leapsecond list from NTC - Updated through IERS Bulletin C69
https://hpiers.obspm.fr/iers/bul/bulc/ntp/leap-seconds.list
File expires on: 28 June 2026
"""


def area(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    radius: int = WGS84_SMAJ_AXIS / 1000,
) -> float:
    """
    Calculate spherical area bounded by two coordinates.

    :param float lat1: lat1
    :param float lon1: lon1
    :param float lat2: lat2
    :param float lon2: lon2
    :param float radius: radius in km (Earth = 6378.137 km)
    :return: area in km²
    :rtype: float
    """

    phi1, phi2 = [c * pi / 180 for c in (lat1, lat2)]
    return pow(radius, 2) * pi * abs(sin(phi1) - sin(phi2)) * abs(lon1 - lon2) / 180


def bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate bearing between two coordinates.

    :param float lat1: lat1
    :param float lon1: lon1
    :param float lat2: lat2
    :param float lon2: lon2
    :return: bearing in degrees
    :rtype: float
    """

    phi1, lambda1, phi2, lambda2 = [c * pi / 180 for c in (lat1, lon1, lat2, lon2)]
    y = sin(lambda2 - lambda1) * cos(phi2)
    x = cos(phi1) * sin(phi2) - sin(phi1) * cos(phi2) * cos(lambda2 - lambda1)
    theta = atan2(y, x)
    brng = (theta * 180 / pi + 360) % 360

    return brng


def calc_checksum(content: object) -> str:
    """
    Calculate checksum for raw NMEA message.

    :param object content: NMEA message content (everything except checksum)
    :return: checksum as hex string
    :rtype: str
    """

    cksum = 0
    for sub in content:
        cksum ^= ord(sub)
    return f"{cksum:02X}"


def date2str(dat: datetime.date, form: str = DT) -> str:
    """
    Convert datetime.date to NMEA formatted string.

    :param datetime.date dat: date
    :param str form: date format DT = ddmmyy, DTL = ddmmyyyy, DM = mmddyy (DT)
    :return: NMEA formatted date string
    :rtype: str
    """

    try:
        if form == DM:
            dform = "%m%d%y"
        elif form == DTL:
            dform = "%d%m%Y"
        else:
            dform = "%d%m%y"
        return dat.strftime(dform)
    except (AttributeError, TypeError, ValueError):
        return ""


def date2utc(dates: str, form: str = DT) -> datetime.date:
    """
    Convert NMEA Date to UTC datetime.

    :param str dates: NMEA date
    :param str form: date format DT = ddmmyy, DTL = ddmmyyyy, DM = mmddyy (DT)
    :return: UTC date YYyy:mm:dd
    :rtype: datetime.date
    """

    try:
        if form == "DM":
            dform = "%m%d%y"
        elif form == "DTL":
            dform = "%d%m%Y"
        else:
            dform = "%d%m%y"
        utc = datetime.strptime(dates, dform)
        return utc.date()
    except (TypeError, ValueError):
        return ""


def ddd2dmm(degrees: float, att: str, hpmode: bool = False) -> str:
    """
    Convert decimal degrees to native NMEA degrees decimal
    minutes string (NB: standard NMEA only supports 5dp
    minutes precision - a high precision mode offers 7dp
    precision but this may not be accepted by all NMEA parsers).

    :param float degrees: degrees
    :param str att: 'LA' (lat) or 'LN' (lon)
    :param bool hpmode: high precision mode (7dp rather than 5dp)
    :return: degrees as (d)ddmm.mmmmm(mm) formatted string
    :rtype: str

    """

    try:
        degrees = abs(degrees)
        degrees, minutes = divmod(degrees * 60, 60)
        degrees = int(degrees * 100)
        if hpmode:
            if att == LA:
                dmm = f"{degrees + minutes:.7f}".zfill(12)
            else:  # LN
                dmm = f"{degrees + minutes:.7f}".zfill(13)
        else:
            if att == LA:
                dmm = f"{degrees + minutes:.5f}".zfill(10)
            else:  # LN
                dmm = f"{degrees + minutes:.5f}".zfill(11)
        return dmm
    except (TypeError, ValueError):
        return ""


def deg2dmm(degrees: float, att: str) -> str:
    """
    Convert decimal degrees to degrees decimal minutes string
    e.g. '51°20.76′S'.

    :param float degrees: degrees
    :param str att: 'LA' (lat) or 'LN' (lon)
    :return: degrees as dm.m formatted string
    :rtype: str

    """

    try:
        negative = degrees < 0
        degrees = abs(degrees)
        degrees, minutes = divmod(degrees * 60, 60)
        if negative:
            sfx = "S" if att == LA else "W"
        else:
            sfx = "N" if att == LA else "E"
        return f"{int(degrees)}\u00b0{round(minutes,7)}\u2032{sfx}"
    except (TypeError, ValueError):
        return ""


def deg2dms(degrees: float, att: str) -> str:
    """
    Convert decimal degrees to degrees minutes seconds string
    e.g. '51°20′45.6″N'

    :param float degrees: degrees
    :param str att: 'LA' (lat) or 'LN' (lon)
    :return: degrees as d.m.s formatted string
    :rtype: str

    """

    try:
        negative = degrees < 0
        degrees = abs(degrees)
        minutes, seconds = divmod(degrees * 3600, 60)
        degrees, minutes = divmod(minutes, 60)
        if negative:
            sfx = "S" if att == LA else "W"
        else:
            sfx = "N" if att == LA else "E"
        return f"{int(degrees)}\u00b0{int(minutes)}\u2032{round(seconds,5)}\u2033{sfx}"
    except (TypeError, ValueError):
        return ""


def dmm2ddd(pos: str) -> float:
    """
    Convert NMEA lat/lon string to (unsigned) decimal degrees.

    :param str pos: (d)ddmm.mmmmm
    :return: pos as decimal degrees
    :rtype: float or str if invalid

    """

    try:
        dp = pos.find(".")
        if dp < 4:
            raise ValueError()
        posdeg = float(pos[0 : dp - 2])
        posmin = float(pos[dp - 2 :])
        return round((posdeg + posmin / 60), 10)
    except (TypeError, ValueError):
        return ""


def dms2deg(
    dmsstr: str,
    rnd: int = 7,
) -> float:
    """
    Convert degrees, minutes, seconds string to decimal degrees.

    Expects degrees and (optional) minutes and seconds to be delimited by
    non-numeric char, e.g.

    '51°20′45.6″N' -> 51.346

    '51°30.0′' -> 51.5

    :param str dmsstr: d,m,s string
    :param int rnd: decimal places (7)
    :return: degrees as d.dd
    :rtype: float
    :raises: ValueError if invalid dms string format
    """

    dmsstr = dmsstr.replace(" ", "")
    if (
        re.match(
            r"^([\d.]+[^\d.]{1}){1}([\d.]+[^\d.]{1})?([\d.]+[^\d.]{1})?[NSEW]?$", dmsstr
        )
        is None
    ):
        raise ValueError(f"Invalid dms string format {dmsstr}")

    sign = -1 if dmsstr.find("S") >= 0 or dmsstr.find("W") >= 0 else 1
    dms = re.split(r"[^\d.]", dmsstr, maxsplit=3)
    ddd = 0.0
    for x in range(len(dms) - 1):
        ddd += 0.0 if dms[x] == "" else float(dms[x]) / pow(60, x)
    return round(ddd * sign, rnd)


def ecef2llh(
    x: float,
    y: float,
    z: float,
    a: float = WGS84_SMAJ_AXIS,
    f: float = WGS84_FLATTENING,
) -> tuple:
    """
    Convert ECEF coordinates to geodetic (LLH) using Olson algorithm.

    Olson, D. K. (1996). Converting Earth-Centered, Earth-Fixed Coordinates to
    Geodetic Coordinates. IEEE Transactions on Aerospace and Electronic Systems,
    32(1), 473-476. https://doi.org/10.1109/7.481290

    :param float x: X coordinate
    :param float y: Y coordinate
    :param float z: Z coordinate
    :param float a: semi-major axis (6378137.0 for WGS84)
    :param float f: flattening (298.257223563 for WGS84)
    :return: tuple of (lat, lon, ellipsoidal height in m) as floats
    :rtype: tuple
    """
    # pylint: disable=too-many-locals

    # commented default values are for WGS84 spheroid
    f = 1 / f
    e2 = f * (2 - f)  # 6.6943799901377997e-3
    a1 = a * e2  # 4.2697672707157535e4
    a2 = a1 * a1  # 1.8230912546075455e9
    a3 = a1 * e2 / 2  # 1.8230912546075455e9
    a4 = 2.5 * a2  # 4.5577281365188637e9
    a5 = a1 + a3  # 4.2840589930055659e4
    a6 = 1 - e2  # 9.9330562000986220e-1
    zp = abs(z)
    w2 = x * x + y * y
    w = sqrt(w2)
    z2 = z * z
    r2 = w2 + z2
    r = sqrt(r2)

    # algorithm inaccurate near Earth's core
    # so nominal value returned
    if r < 100000.0:
        return 0.0, 0.0, -1.0e7

    lon = atan2(y, x)
    s2 = z2 / r2
    c2 = w2 / r2
    u = a2 / r
    v = a3 - a4 / r
    if c2 > 0.3:
        s = (zp / r) * (1.0 + c2 * (a1 + u + s2 * v) / r)
        lat = asin(s)
        ss = s * s
        c = sqrt(1.0 - ss)
    else:
        c = (w / r) * (1.0 - s2 * (a5 - u - c2 * v) / r)
        lat = acos(c)
        ss = 1.0 - c * c
        s = sqrt(ss)
    g = 1.0 - e2 * ss
    rg = a / sqrt(g)
    rf = a6 * rg
    u = w - rg * c
    v = zp - rf * s
    f = c * u + s * v
    m = c * v - s * u
    p = m / (rf / g + f)
    lat = lat + p
    height = f + m * p / 2.0
    if z < 0.0:
        lat = -lat

    lat, lon = [c * 180 / pi for c in (lat, lon)]
    return lat, lon, height


def generate_checksum(talker: str, msgID: str, payload: list) -> str:
    """
    Generate checksum for new NMEA message.

    :param str talker: talker e.g. "GN"
    :param str msgID: msgID e.g. "GLL"
    :param list payload: payload as list
    :return: checksum as hex string
    :rtype: str
    """

    content = talker + msgID
    for field in payload:
        content += f",{field}"
    return calc_checksum(content)


def get_gpswnotow(dat: datetime) -> tuple:
    """
    Get GPS Week number (Wno) and Time of Week (Tow)
    for midnight on given date.

    GPS Epoch 0 = 6th Jan 1980

    :param datetime dat: calendar date
    :return: tuple of (Wno, Tow)
    :rtype: tuple
    """

    wno = int((dat - GPSEPOCH0).days / 7)
    tow = ((dat.weekday() + 1) % 7) * 86400
    return wno, tow


def get_parts(message: object) -> tuple:
    """
    Get content, talker, msgid, payload and checksum of raw NMEA message.

    :param object message: entire message as bytes or string
    :return: tuple of (content, talker, msgID, payload as list, checksum)
    :rtype: tuple
    :raises: NMEAMessageError (if message is badly formed)
    """

    try:
        if isinstance(message, bytes):
            message = message.decode("utf-8")
        content, cksum = message.strip("$\r\n").split("*", 1)
        hdr, *payload = content.split(",")
        s = 1 if hdr[:1] == "P" else 2
        talker, msgid = hdr[:s], hdr[s:]
        return content, talker, msgid, payload, cksum
    except Exception as err:
        raise nme.NMEAMessageError(f"Badly formed message {message}") from err


def haversine(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    radius: int = WGS84_SMAJ_AXIS / 1000,
) -> float:
    """
    Calculate spherical distance in km between two coordinates using haversine formula.

    NB suitable for coordinates greater than around 50m apart. For
    smaller separations, use the planar approximation formula.

    :param float lat1: lat1
    :param float lon1: lon1
    :param float lat2: lat2
    :param float lon2: lon2
    :param float radius: radius in km (Earth = 6378.137 km)
    :return: spherical distance in km
    :rtype: float
    """

    phi1, lambda1, phi2, lambda2 = [c * pi / 180 for c in (lat1, lon1, lat2, lon2)]
    dist = radius * acos(
        cos(phi2 - phi1) - cos(phi1) * cos(phi2) * (1 - cos(lambda2 - lambda1))
    )

    return dist


def hex2str(num: int, padding: int = 0) -> str:
    """
    Convert hex integer to padded or unpadded string format,
    as used by some proprietary NMEA message types.

    :param int num: hexadecimal integer
    :param padding: no of padded digits (0)
    :return: integer as string
    :rtype: str
    """

    pad = f"{padding:02d}" if padding else ""
    return f"{num:{pad}x}".upper()


def knots2spd(knots: float, unit: str = "MS") -> float:
    """
    Convert speed in knots to speed in specified units.

    :param float knots: knots
    :param unit str: 'MS' (default), 'FS', MPH', 'KMPH'
    :return: speed in m/s, feet/s, mph or kmph
    :rtype: float

    """

    try:
        return knots * KNOTSCONV[unit.upper()]
    except KeyError as err:
        raise KeyError(
            f"Invalid conversion unit {unit.upper()} - must be in {list(KNOTSCONV.keys())}."
        ) from err
    except TypeError as err:
        raise TypeError(
            f"Invalid knots value {knots} - must be float or integer."
        ) from err


def latlon2dmm(lat: float, lon: float) -> tuple:
    """
    Converts decimal lat/lon tuple to degrees decimal minutes.

    :param float lat: lat
    :param float lon: lon
    :return: (lat,lon) in d.mm.m format
    :rtype: tuple
    """

    lat = deg2dmm(lat, LA)
    lon = deg2dmm(lon, LN)
    return lat, lon


def latlon2dms(lat: float, lon: float) -> tuple:
    """
    Converts decimal lat/lon tuple to degrees minutes seconds.

    :param float lat: lat
    :param float lon: lon
    :return: (lat,lon) in d.m.s. format
    :rtype: tuple
    """

    lat = deg2dms(lat, LA)
    lon = deg2dms(lon, LN)
    return lat, lon


def leapsecond(dat: datetime) -> int:
    """
    Get GPS UTC leapsecond offset effective at date.

    Refer to LEAPSECONDS constant.

    - LEAPS0 = 1900-01-01 00:00:00
    - GPSEPOCH0 = 1980-01-06: 00:00:00

    :param datetime.datetime dat: effective date
    :return: leapsecond offset
    :rtype: int
    """

    def totsec(dt) -> int:
        return (dt - LEAPS0).total_seconds()

    if totsec(dat) < LEAPSECONDS[0][0]:
        return 0

    dts = []
    for dt in (dat, GPSEPOCH0):
        dts.append(max((val for key, val in LEAPSECONDS if key < totsec(dt))))
    return dts[0] - dts[1]


def llh2ecef(
    lat: float,
    lon: float,
    height: float,
    a: float = WGS84_SMAJ_AXIS,
    f: float = WGS84_FLATTENING,
) -> tuple:
    """
    Convert geodetic coordinates (LLH) to ECEF.

    :param float lat: lat in degrees
    :param float lon: lon on degrees
    :param float height: ellipsoidal height in metres
    :param float a: semi-major axis (6378137.0 for WGS84)
    :param float f: flattening (298.257223563 for WGS84)
    :return: tuple of ECEF (X, Y, Z) as floats
    :rtype: tuple
    """

    lat, lon = [c * pi / 180 for c in (lat, lon)]

    f = 1 / f
    e2 = f * (2 - f)
    a2 = a**2
    b2 = a2 * (1 - e2)

    N = a / sqrt(1 - e2 * sin(lat) ** 2)
    x = (N + height) * cos(lat) * cos(lon)
    y = (N + height) * cos(lat) * sin(lon)
    z = ((b2 / a2) * N + height) * sin(lat)

    return x, y, z


def llh2iso6709(lat: float, lon: float, alt: float, crs: str = WGS84) -> str:
    """
    Convert decimal degrees and alt to ISO6709 format
    e.g. "+27.5916+086.5640+8850CRSWGS_84/".

    :param float lat: latitude
    :param float lon: longitude
    :param float alt: altitude (hMSL)
    :param float crs: coordinate reference system (default = WGS_84)
    :return: position in ISO6709 format
    :rtype: str

    """

    lati, loni, alti = ["-" if c < 0 else "+" for c in (lat, lon, alt)]
    return f"{lati}{abs(lat)}{loni}{abs(lon)}{alti}{alt}CRS{crs}/"


def msgdesc(msgID: str) -> str:
    """
    Return descriptive string for NMEA msgId.

    :param msgID str: message ID e.g. 'GGA'
    :return: description of message
    :rtype: str

    """
    # pylint: disable=invalid-name

    if msgID in NMEA_MSGIDS:
        return NMEA_MSGIDS[msgID]
    if msgID in NMEA_MSGIDS_PROP:
        return NMEA_MSGIDS_PROP[msgID]
    return f"Unknown msgID {msgID}"


def planar(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
    radius: int = WGS84_SMAJ_AXIS,
) -> float:
    """
    Calculate planar distance between two coordinates using planar
    approximation formula.

    NB suitable for coordinates less than around 50m apart. For
    larger separations, use the haversine great circle formula.

    :param float lat1: lat1
    :param float lon1: lon1
    :param float lat2: lat2
    :param float lon2: lon2
    :param float radius: radius in m (Earth = 6378137 m)
    :return: planar distance in m
    :rtype: float
    """

    phi1, lambda1, phi2, lambda2 = [c * pi / 180 for c in (lat1, lon1, lat2, lon2)]
    dlambda = (lambda2 - lambda1) * cos(phi1)
    dphi = phi2 - phi1
    dist = radius * sqrt(dlambda * dlambda + dphi * dphi)

    return dist


def time2str(tim: datetime.time) -> str:
    """
    Convert datetime.time to NMEA formatted string.

    :param datetime.time tim: time
    :return: NMEA formatted time string hhmmss.ss
    :rtype: str
    """

    try:
        return tim.strftime("%H%M%S.%f")[0:9]
    except (AttributeError, TypeError, ValueError):
        return ""


def time2utc(times: str) -> datetime.time:
    """
    Convert NMEA Time to UTC datetime.

    :param str times: NMEA time hhmmss.ss
    :return: UTC time hh:mm:ss.ss
    :rtype: datetime.time
    """

    try:
        if len(times) == 6:  # decimal seconds is omitted
            times = times + ".00"
        utc = datetime.strptime(times, "%H%M%S.%f")
        return utc.time()
    except (TypeError, ValueError):
        return ""
