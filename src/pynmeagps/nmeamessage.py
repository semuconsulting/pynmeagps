"""
Main NMEA GNSS/GPS Message Protocol Class.

Created on 04 Mar 2021

:author: semuadmin
:copyright: SEMU Consulting © 2021
:license: BSD 3-Clause
"""

# pylint: disable=invalid-name, too-many-instance-attributes, too-many-positional-arguments

import struct
from datetime import datetime, timezone
from logging import getLogger

import pynmeagps.exceptions as nme
import pynmeagps.nmeatypes_core as nmt
import pynmeagps.nmeatypes_get as nmg
import pynmeagps.nmeatypes_get_prop as nmgp
import pynmeagps.nmeatypes_poll as nmp
import pynmeagps.nmeatypes_set as nms
from pynmeagps.nmeahelpers import (
    date2str,
    date2utc,
    ddd2dmm,
    dmm2ddd,
    generate_checksum,
    time2str,
    time2utc,
)


class NMEAMessage:
    """NMEA GNSS/GPS Message Class."""

    def __init__(
        self,
        talker: str,
        msgID: str,
        msgmode: int,
        hpnmeamode: bool = False,
        validate: int = nmt.VALCKSUM,
        userdefined: dict = None,
        **kwargs,
    ):
        """Constructor.

        If 'payload' is passed as a keyword arg, this is taken to contain the entire
        message content as a list of string values; any other keyword args are ignored.

        Otherwise, any individual attributes passed as keyword args will be set to the
        value provided, all others will be assigned a nominal value according to type.

        :param str talker: message talker e.g. "GP" or "P"
        :param str msgID: message ID e.g. "GGA"
        :param int msgmode: mode (0=GET, 1=SET, 2=POLL)
        :param bool hpnmeamode: high precision lat/lon mode (7dp rather than 5dp) (False)
        :param int validate: VALNONE (0), VALCKSUM (1), VALMSGID (2),
            (can be OR'd) (1)
        :param dict userdefined: user-defined payload definition dictionary (None)
        :param kwargs: keyword arg(s) representing all or some payload attributes
        :raises: NMEAMessageError
        """

        # object is mutable during initialisation only
        super().__setattr__("_immutable", False)
        self._logger = getLogger(__name__)
        self._validate = validate
        self._userdefined = {} if userdefined is None else userdefined

        if msgmode not in (0, 1, 2):
            raise nme.NMEAMessageError(
                f"Invalid msgmode {msgmode} - must be 0, 1 or 2."
            )
        if talker not in nmt.NMEA_TALKERS:
            if self._validate & nmt.VALMSGID:
                raise nme.NMEAMessageError(f"Unknown talker {talker}.")
        if msgID in nmt.NMEA_MSGIDS:
            self._defsource = nmt.DEF_STND  # standard
        elif msgID in nmt.NMEA_MSGIDS_PROP or msgID in nmt.NMEA_PREFIX_PROP:
            self._defsource = nmt.DEF_PROP  # proprietary
        elif msgID in self._userdefined:
            self._defsource = nmt.DEF_USER  # user-defined
        else:
            self._defsource = nmt.DEF_UNKN  # unrecognised
            if self._validate & nmt.VALMSGID:
                raise nme.NMEAMessageError(
                    f"Unknown msgID {talker}{msgID}, msgmode {('GET','SET','POLL')[msgmode]}."
                )

        self._mode = msgmode
        # high precision NMEA mode returns NMEA lat/lon to 7dp rather than 5dp
        self._hpnmeamode = hpnmeamode
        self._talker = talker
        self._msgID = msgID
        self._do_attributes(**kwargs)
        self._immutable = True  # once initialised, object is immutable

    def _do_attributes(self, **kwargs):
        """
        Populate NMEAMessage from named attribute keywords.
        Where a named attribute is absent, set to a nominal value (zeros or blanks).

        :param kwargs: optional content key/value pairs
        :raises: UBXTypeError
        """

        pindex = 0  # payload index
        gindex = []  # (nested) grouped attribute indices

        try:
            self._payload = kwargs.get("payload", [])
            self._checksum = kwargs.get("checksum", None)
            pdict = self._get_dict(**kwargs)  # get payload definition dict
            if pdict is None:  # definition not yet implemented
                if "payload" in kwargs:
                    self._set_attribute_nominal(kwargs["payload"])
                return
            for key in pdict.keys():  # process each attribute in dict
                (pindex, gindex) = self._set_attribute(
                    pindex, pdict, key, gindex, **kwargs
                )
            # generate checksum for newly-created message
            if self._checksum is None:
                self._checksum = generate_checksum(
                    self._talker, self._msgID, self._payload
                )

        except (
            AttributeError,
            OverflowError,
            struct.error,
            TypeError,
            ValueError,
        ) as err:
            raise nme.NMEATypeError(
                f"Incorrect type for attribute {key} in msgID {self._msgID}."
            ) from err

    def _set_attribute(
        self, pindex: int, pdict: dict, key: str, gindex: list, **kwargs
    ) -> tuple:
        """
        Recursive routine to set individual or grouped payload attributes.

        :param int pindex: payload index
        :param dict pdict: dict representing payload definition
        :param str key: attribute keyword
        :param list gindex: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: (pindex, gindex[])
        :rtype: tuple
        """

        att = pdict[key]  # get attribute type
        if isinstance(att, tuple):  # repeating group of attributes
            (pindex, gindex) = self._set_attribute_group(att, pindex, gindex, **kwargs)
        else:  # single attribute
            pindex = self._set_attribute_single(att, pindex, key, gindex, **kwargs)

        return (pindex, gindex)

    def _set_attribute_group(
        self, att: tuple, pindex: int, gindex: list, **kwargs
    ) -> tuple:
        """
        Process (nested) group of attributes.

        :param tuple att: attribute group - tuple of (num repeats, attribute dict)
        :param int pindex: payload index
        :param list gindex: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: (pindex, gindex[])
        :rtype: tuple
        """

        gindex.append(0)  # add a (nested) group index
        numr, attd = att  # number of repeats, group dictionary

        # derive or retrieve number of items in group
        if isinstance(numr, int):  # fixed number of repeats
            rng = numr
        elif numr == "None":  # indeterminate number of repeats
            pindexend = 0  # may need tweaking
            rng = self._calc_num_repeats(attd, self._payload, pindex, pindexend)
        else:  # number of repeats is defined in named attribute
            rng = getattr(self, numr)
        # recursively process each group attribute,
        # incrementing the payload index and group index as we go
        for i in range(rng):
            gindex[-1] = i + 1
            for key1 in attd.keys():
                (pindex, gindex) = self._set_attribute(
                    pindex, attd, key1, gindex, **kwargs
                )

        gindex.pop()  # remove this (nested) group index

        return (pindex, gindex)

    def _set_attribute_single(
        self, att: str, pindex: int, key: str, gindex: list, **kwargs
    ) -> int:
        """
        Set individual attribute value.

        :param str att: attribute type e.g. 'NU'
        :param int pindex: payload index
        :param str key: attribute keyword
        :param list gindex: repeating group index array
        :param kwargs: optional payload key/value pairs
        :return: pindex
        :rtype: int
        """
        # pylint: disable=no-member, access-member-before-definition, attribute-defined-outside-init

        # if attribute is part of a (nested) repeating group, suffix name with group index
        keyr = key
        for i in gindex:  # one index for each nested level
            if i > 0:
                keyr += f"_{i:02d}"

        try:
            # all attribute values have been provided
            if "payload" in kwargs:
                val = self._payload[pindex]
                val = self.str2val(val, att)
            # some attribute values have been provided,
            # the rest will be set to a nominal value
            else:
                if att == nmt.LND and hasattr(self, "lon"):
                    if isinstance(self.lon, (int, float)):
                        val = "W" if self.lon < 0 else "E"
                    else:  # pragma: no cover
                        val = "E"
                elif att == nmt.LAD and hasattr(self, "lat"):
                    if isinstance(self.lat, (int, float)):
                        val = "S" if self.lat < 0 else "N"
                    else:  # pragma: no cover
                        val = "N"
                else:
                    val = kwargs.get(keyr, self.nomval(att))
                vals = self.val2str(val, att, self._hpnmeamode)
                self._payload.append(vals)

        except (
            IndexError
        ):  # probably just an older device missing NMEA <=4.10 dict attributes
            return pindex

        setattr(self, keyr, val)  # add attribute to NMEAMessage object
        if "payload" in kwargs:
            # override sign of lat/lon according to NS and EW values
            if att == nmt.LND and hasattr(self, "lon"):
                if isinstance(self.lon, (int, float)):
                    self.lon = -abs(self.lon) if val == "W" else abs(self.lon)
            elif att == nmt.LAD and hasattr(self, "lat"):
                if isinstance(self.lat, (int, float)):
                    self.lat = -abs(self.lat) if val == "S" else abs(self.lat)
        pindex += 1  # move on to next attribute in payload definition

        return pindex

    def _set_attribute_nominal(self, payload: list):
        """
        Set nominal attributes for unrecognised NMEA sentence types.

        :param list payload: payload as list
        """

        for i, fld in enumerate(payload):
            setattr(self, f"field_{i+1:02d}", fld)

    def _get_dict(self, **kwargs) -> dict:
        """
        Get payload dictionary.

        :return: dictionary representing payload definition
        :rtype: dict
        """

        try:
            key = self.msgID
            if key in nmt.NMEA_PREFIX_PROP:  # proprietary, first element is msgId
                if "payload" in kwargs:
                    if key == "ASHR" and self._payload[0][1].isdigit():
                        pass  # exception for PASHR pitch and roll sentence without msgId
                    else:
                        key += self._payload[0]
                elif "msgId" in kwargs:
                    key += kwargs["msgId"]
                else:
                    raise nme.NMEAMessageError(
                        f"P{key} message definitions must "
                        "include payload or msgId keyword arguments."
                    )
            key = key.upper()
            if self._mode == nmt.POLL:
                return nmp.NMEA_PAYLOADS_POLL[key]
            if self._mode == nmt.SET:
                return nms.NMEA_PAYLOADS_SET[key]
            if self._defsource == nmt.DEF_PROP:  # proprietary
                return nmgp.NMEA_PAYLOADS_GET_PROP[key]
            if self._defsource == nmt.DEF_USER:  # user defined
                return self._userdefined[key]
            return nmg.NMEA_PAYLOADS_GET[key]  # standard
        except KeyError as err:
            erm = f"Unknown msgID {key} msgmode {('GET', 'SET', 'POLL')[self._mode]}."
            if self._validate & nmt.VALMSGID:
                raise nme.NMEAMessageError(erm) from err
            return None  # message not yet implemented

    def _calc_num_repeats(
        self, attd: dict, payload: list, pindex: int, pindexend: int = 0
    ) -> int:
        """
        Deduce number of items in repeating group.

        :param dict attd: grouped attribute dictionary
        :param list payload : content as list
        :param int pindex: number of payload attributes before group
        :param int pindexend: number of payload attributes after group
        :return: number of repeats
        :rtype: int
        """

        lenpayload = len(payload) - pindex - pindexend
        lengroup = len(attd)
        return int(lenpayload / lengroup)

    def __str__(self) -> str:
        """
        Human readable representation.

        :return: human readable representation
        :rtype: str
        """

        stg = f"<NMEA({self.identity}"
        stg += ", "
        if self._defsource == nmt.DEF_UNKN:
            stg += "NOMINAL, "
        for i, att in enumerate(self.__dict__):
            if att[0] != "_":  # only show public attributes
                val = self.__dict__[att]
                stg += att + "=" + str(val)
                if i < len(self.__dict__) - 1:
                    stg += ", "
        stg += ")>"

        return stg

    def __repr__(self) -> str:
        """
        Machine readable representation.

        eval(repr(obj)) = obj

        :return: machine readable representation
        :rtype: str
        """

        return (
            f"NMEAMessage('{self._talker}','{self._msgID}', "
            f"{self._mode}, payload={self._payload})"
        )

    def __setattr__(self, name, value):
        """
        Override setattr to make object immutable after instantiation.

        :param str name: attribute name
        :param object value: attribute value
        :raises: NMEAMessageError
        """

        if self._immutable:
            raise nme.NMEAMessageError(
                f"Object is immutable. Updates to {name} not permitted after initialisation."
            )

        super().__setattr__(name, value)

    def serialize(self) -> bytes:
        """
        Serialize message.

        :return: serialized output
        :rtype: bytes
        """

        output = "$" + self._talker + self._msgID + ","
        for i, s in enumerate(self._payload):
            output += ("," if i else "") + s
        output += "*" + self._checksum + "\r\n"
        return output.encode("utf-8")  # convert str to bytes

    @property
    def identity(self) -> str:
        """
        Identity getter.

        :return: message identity e.g. GNGSA
        :rtype: str
        """

        # pylint: disable=no-member

        if (
            self._talker == "P"
            and self._msgID in nmt.NMEA_PREFIX_PROP
            and hasattr(self, "msgId")
        ):
            return self._talker + self._msgID + self.msgId
        return self._talker + self._msgID

    @property
    def talker(self) -> str:
        """
        Talker getter.

        :return: talker e.g. GN
        :rtype: str
        """

        return self._talker

    @property
    def msgID(self) -> str:
        """
        Message id getter.

        :return: message id e.g. GSA
        :rtype: str
        """

        return self._msgID

    @property
    def msgmode(self) -> int:
        """
        Message mode getter.

        :return: message mode
        :rtype: int
        """

        return self._mode

    @property
    def payload(self) -> list:
        """
        Payload getter.

        :return: raw payload as list of strings
        :rtype: list
        """

        return self._payload

    @property
    def checksum(self) -> str:
        """
        Checksum getter.

        :return: checksum as hex string
        :rtype: str
        """

        return self._checksum

    @staticmethod
    def str2val(vals: str, att: str) -> object:
        """
        Convert NMEA string to typed value
        (this is the format that will be available to end users).

        :param str vals: attribute value in NMEA protocol format
        :param str att: attribute type e.g. 'DE'
        :return: attribute value
        :rtype: object
        :raises: MMEATypeError
        """

        val = vals
        if att in (nmt.CH, nmt.ST, nmt.LAD, nmt.LND):
            pass
        elif att == nmt.HX:
            val = vals
        elif att == nmt.DE:  # decimal
            if vals != "":
                val = float(vals)
        elif att in (nmt.DT, nmt.DM):  # date
            val = date2utc(vals, att)
        elif att == nmt.IN:  # integer
            if vals != "":
                val = int(vals)
        elif att in (nmt.LA, nmt.LN):  # lat/lon (d)ddmm.mmmmm(mm)
            val = dmm2ddd(vals)
        elif att == nmt.TM:  # time hhmmss.ss
            val = time2utc(vals)
        else:
            raise nme.NMEATypeError(f"Unknown attribute type {att}.")
        return val

    @staticmethod
    def val2str(val, att: str, hpmode: bool = False) -> str:
        """
        Convert typed value to NMEA string
        (this is the format used internally by the NMEA protocol).

        :param object val: typed attribute value
        :param str att: attribute type e.g. 'IN'
        :param bool hpmode: high precision lat/lon mode (7dp rather than 5dp)
        :return: attribute value in NMEA protocol format
        :rtype: str
        :raises: NMEATypeError

        """

        if att in (nmt.CH, nmt.ST, nmt.LAD, nmt.LND):
            vals = str(val)
        elif att == nmt.HX:
            vals = str(val)
        elif att == nmt.DE:
            vals = str(val)
        elif att == nmt.IN:
            vals = str(val)
        elif att in (nmt.LA, nmt.LN):
            vals = ddd2dmm(val, att, hpmode)
        elif att == nmt.TM:
            vals = time2str(val)
        elif att in (nmt.DT, nmt.DTL, nmt.DM):
            vals = date2str(val, att)
        else:
            raise nme.NMEATypeError(f"Unknown attribute type {att}.")
        return vals

    @staticmethod
    def nomval(att: str) -> object:
        """
        Return nominal value for specified attribute type

        :param str att: attribute type e.g. 'DE'
        :return: nominal value for type
        :rtype: object
        :raises: NMEATypeError
        """

        if att in (nmt.CH, nmt.ST, nmt.LA, nmt.LN):
            val = ""
        elif att == nmt.LAD:  # pragma: no cover
            val = "N"
        elif att == nmt.LND:  # pragma: no cover
            val = "E"
        elif att == nmt.HX:
            val = "0"
        elif att == nmt.DE:
            val = 0.0
        elif att == nmt.IN:
            val = 0
        elif att == nmt.TM:
            val = datetime.now(timezone.utc).time()
        elif att in (nmt.DT, nmt.DTL, nmt.DM):
            val = datetime.now(timezone.utc).date()
        else:
            raise nme.NMEATypeError(f"Unknown attribute type {att}.")
        return val
