"""
NMEA Custom Exception Types

Created on 04 Mar 2021

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""


class NMEAParseError(Exception):
    """
    NMEA Parsing error.
    """


class NMEAStreamError(Exception):
    """
    NMEA Streaming error.
    """


class NMEAMessageError(Exception):
    """
    NMEA Undefined message class/id.
    Essentially a prompt to add missing payload types to UBX_PAYLOADS.
    """


class NMEATypeError(Exception):
    """
    NMEA Undefined payload attribute type.
    Essentially a prompt to fix incorrect payload definitions to UBX_PAYLOADS.
    """
