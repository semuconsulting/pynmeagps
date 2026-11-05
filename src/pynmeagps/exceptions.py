"""
NMEA Custom Exception Types

Created on 04 Mar 2021

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2020
:license: BSD 3-Clause
"""


class NMEAError(Exception):
    """
    NMEA Generic error.
    """


class NMEAParseError(NMEAError):
    """
    NMEA Parsing error.
    """


class NMEAStreamError(NMEAError):
    """
    NMEA Streaming error.
    """


class NMEAMessageError(NMEAError):
    """
    NMEA Undefined message class/id.
    Essentially a prompt to add missing payload types to UBX_PAYLOADS.
    """


class NMEATypeError(NMEAError):
    """
    NMEA Undefined payload attribute type.
    Essentially a prompt to fix incorrect payload definitions to UBX_PAYLOADS.
    """
