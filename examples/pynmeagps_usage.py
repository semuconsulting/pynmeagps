"""
pynmeagps_usage.py

Examples of pynmeagps.NMEAMessage constructors.

Created on 19 Aug 2024

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2021
:license: BSD 3-Clause
"""

from datetime import datetime

from pynmeagps import SET, NMEAMessage

# NOTE THAT LAD ("N"/"S") and LND ("E"/"W") attributes do not need to be explicitly
# provided - these values will be derived from the sign of the decimal lat/lon values.

# NMEA Date (DM, DT, DTL) and Time (TM) attributes can be populated in any of the following ways:

# A) use formatted string types for TM and DT attributes
msg1 = NMEAMessage(
    "P",
    "GRMI",
    SET,
    lat=-115.81513,
    lon=37.23345,
    date="2025-09-12",  # "-" delimiters are optional
    time="12:15:34",  # ":" delimiters are optional
    rcvr_cmd="D",
)
# <NMEA(PGRMI, lat=-115.81513, NS=S, lon=37.23345, EW=E, date=2025-09-12, time=12:15:34, rcvr_cmd=D)>
# b'$PGRMI,11548.90780,S,03714.00700,E,120925,121534,D*3B\r\n'
print(msg1)
print(msg1.serialize())

# B) use datetime.date() and datetime.time() types for DT and TM attributes
msg2 = NMEAMessage(
    "P",
    "GRMI",
    SET,
    lat=-115.81513,
    lon=37.23345,
    date=datetime(2025, 9, 12).date(),
    time=datetime(2025, 9, 12, 12, 15, 34).time(),
    rcvr_cmd="D",
)
# <NMEA(PGRMI, lat=-115.81513, NS=S, lon=37.23345, EW=E, date=2025-09-12, time=12:15:34, rcvr_cmd=D)>
# b'$PGRMI,11548.90780,S,03714.00700,E,120925,121534.00,D*15\r\n'
print(msg2)
print(msg2.serialize())

# C) use default values
msg3 = NMEAMessage(
    "P",
    "GRMI",
    SET,
    lat=-115.81513,
    lon=37.23345,
    rcvr_cmd="D",
)
# <NMEA(PGRMI, lat=-115.81513, NS=S, lon=37.23345, EW=E, date=2025-09-18, time=14:37:20.373212, rcvr_cmd=D)>
# b'$PGRMI,11548.90780,S,03714.00700,E,180925,143720.37,D*18\r\n'
print(msg3)
print(msg3.serialize())
