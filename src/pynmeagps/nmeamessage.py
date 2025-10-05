"""
Main NMEA GNSS/GPS Message Protocol Class.

Created on 04 Mar 2021

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2021
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
import pynmeagps.nmeatypes_poll_prop as nmpp
import pynmeagps.nmeatypes_set as nms
import pynmeagps.nmeatypes_set_prop as nmsp
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
                # remove group delimiters in proprietary PSSNSNC message
                if self.identity == "PSSNSNC":
                    self._payload[pindex] = (
                        self._payload[pindex].replace("[", "").replace("]", "")
                    )
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
                    val = kwargs.get(keyr, self.nomval(att, self.msgmode))
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

        dic = None
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

            if self._defsource == nmt.DEF_PROP:  # proprietary
                dic = self._get_dict_prop(key, **kwargs)
            elif self._defsource == nmt.DEF_USER:  # user defined
                dic = self._userdefined[key]
            else:  # standard
                if self._mode == nmt.POLL:
                    dic = nmp.NMEA_PAYLOADS_POLL[key]
                elif self._mode == nmt.SET:  # pragma: no cover
                    dic = nms.NMEA_PAYLOADS_SET[key]
                else:
                    dic = nmg.NMEA_PAYLOADS_GET[key]
        except KeyError as err:  # unknown msgid
            erm = f"Unknown msgID {key} msgmode {('GET', 'SET', 'POLL')[self._mode]}."
            if self._validate & nmt.VALMSGID:
                raise nme.NMEAMessageError(erm) from err

        return dic

    def _get_dict_prop(self, key: str, **kwargs) -> dict:
        """
        Get payload dictionary for proprietary message types.

        :param str key: msgid
        :return: dictionary representing payload definition
        :rtype: dict
        """

        if key == "QTMCFGGEOFENCE":
            key = self._get_dict_qtmcfggeofence(key, self._mode, **kwargs)
        elif key == "QTMCFGMSGRATE":
            key = self._get_dict_qtmcfgmsgrate(key, self._mode, **kwargs)
        elif key == "QTMCFGPPS":
            key = self._get_dict_qtmcfgpps(key, self._mode, **kwargs)
        elif key == "QTMCFGSAT":
            key = self._get_dict_qtmcfgsat(key, self._mode, **kwargs)
        elif key == "QTMCFGUART":
            key = self._get_dict_qtmcfguart(key, self._mode, **kwargs)
        elif key == "QTMSN":
            key = self._get_dict_qtmsn(key, self._mode, **kwargs)
        elif key == "STMDRSENMSG":
            key = self._get_dict_stmdrsenmsg(key, self._mode, **kwargs)
        elif key[0:3] == "QTM":
            key = self._get_dict_qtmacknak(key, self._mode)

        if self._mode == nmt.POLL:
            return nmpp.NMEA_PAYLOADS_POLL_PROP[key]
        if self._mode == nmt.SET:
            return nmsp.NMEA_PAYLOADS_SET_PROP[key]
        return nmgp.NMEA_PAYLOADS_GET_PROP[key]

    def _get_dict_qtmcfguart(self, key: str, mode: int, **kwargs) -> str:
        """
        Get payload dictionary for proprietary Quectel QTMCFGUART
        command and query variants.

        :param str key: msgid
        :param int mode: msgmode 1/2
        :return: key of payload definition
        :rtype: str
        """

        lp = len(self._payload)
        py = "payload" in kwargs
        pt = "portid" in kwargs
        if mode == nmt.SET:
            bd = "baudrate" in kwargs
            db = "databit" in kwargs
            if (py and lp == 2) or (not py and not pt and bd and not db):
                key += "_CURRBAUD"
            elif (py and lp == 3) or (not py and pt and bd and not db):
                key += "_BAUD"
            elif (py and lp == 6) or (not py and not pt and bd and db):
                key += "_CURR"
        elif mode == nmt.POLL:
            if (py and lp == 1) or (not py and not pt):
                key += "_CURR"
        return key

    def _get_dict_qtmcfgmsgrate(self, key: str, mode: int, **kwargs) -> str:
        """
        Get payload dictionary for proprietary Quectel QTMCFGMSGRATE
        command and query variants.

        :param str key: msgid
        :param int mode: msgmode 1/2
        :return: key of payload definition
        :rtype: str
        """

        lp = len(self._payload)
        py = "payload" in kwargs
        mv = "msgver" in kwargs
        pt = "porttype" in kwargs
        if mode in (nmt.SET, nmt.GET):
            if (py and lp == 3) or (not py and not pt and not mv):
                key += "_NOVER"
            elif (py and lp == 5) or (not py and pt and not mv):
                key += "_INTFNOVER"
            elif (py and lp == 6) or (not py and pt and mv):
                key += "_INTF"
        elif mode == nmt.POLL:
            if (py and lp == 2) or (not py and not pt and not mv):
                key += "_NOVER"
            elif (py and lp == 4) or (not py and pt and not mv):
                key += "_INTFNOVER"
            elif (py and lp == 5) or (not py and pt and mv):
                key += "_INTF"
        return key

    def _get_dict_qtmcfgpps(self, key: str, mode: int, **kwargs) -> str:
        """
        Get payload dictionary for proprietary Quectel QTMCFGPPS
        command and query variants.

        :param str key: msgid
        :param int mode: msgmode 1/2
        :return: key of payload definition
        :rtype: str
        """

        lp = len(self._payload)
        py = "payload" in kwargs
        if mode == nmt.SET:
            if (py and lp == 3) or (not py and kwargs.get("enable", 1) == 0):
                key += "_DIS"
        return key

    def _get_dict_qtmcfgsat(self, key: str, mode: int, **kwargs) -> str:
        """
        Get payload dictionary for proprietary Quectel QTMCFGSAT
        command and query variants.

        :param str key: msgid
        :param int mode: msgmode 1/2
        :return: key of payload definition
        :rtype: str
        """

        lp = len(self._payload)
        py = "payload" in kwargs
        mh = "maskhigh" in kwargs
        if mode == nmt.SET:
            if (py and lp == 4) or (not py and not mh):
                key += "_LOW"
        elif mode == nmt.GET:
            if (py and lp == 4) or (not py and not mh):
                key += "_LOW"
            elif lp in (1, 2):
                key = self._get_dict_qtmacknak(key, mode)
        return key

    def _get_dict_qtmcfggeofence(self, key: str, mode: int, **kwargs) -> str:
        """
        Get payload dictionary for proprietary Quectel QTMCFGGEOFENCE
        command and query variants.

        :param str key: msgid
        :param int mode: msgmode 1/2
        :return: key of payload definition
        :rtype: str
        """

        lp = len(self._payload)
        py = "payload" in kwargs
        l1 = "lon1" in kwargs
        if mode == nmt.SET:
            if (py and lp == 13) or (not py and l1):
                key += "_POLY"
            elif (py and lp == 3) or (not py and kwargs.get("geofencemode", 1) == 0):
                key += "_DIS"
        elif mode == nmt.GET:
            if (py and lp == 13) or (not py and l1):
                key += "_POLY"
            elif lp in (1, 2):
                key = self._get_dict_qtmacknak(key, mode)
        return key

    def _get_dict_qtmsn(self, key: str, mode: int, **kwargs) -> str:
        """
        Get payload dictionary for proprietary Quectel QTMSN.
        (bug in LG580P firmware - seems to transpose status field?)

        :param str key: msgid
        :param int mode: msgmode 1/2
        :return: key of payload definition
        :rtype: str
        """

        py = "payload" in kwargs
        if mode == nmt.GET:
            if py and kwargs["payload"][0].isnumeric():
                key += "_ALT"
        return key

    def _get_dict_stmdrsenmsg(self, key: str, mode: int, **kwargs) -> str:
        """
        Get payload dictionary for proprietary Quectel PSTMDRSENMSG variants.

        :param str key: msgid
        :param int mode: msgmode 1/2
        :return: key of payload definition
        :rtype: str
        """

        py = "payload" in kwargs
        mt = "msgtype" in kwargs
        msgtype = ""
        if py:
            msgtype = self._payload[0]
        elif not py and mt:
            msgtype = kwargs["msgtype"]
        key += f"_{msgtype}"
        return key

    def _get_dict_qtmacknak(self, key: str, mode: int) -> str:
        """
        Get payload dictionary for proprietary Quectel command
        response variants.

        :param str key: msgid
        :param int mode: msgmode 1/2
        :return: key of payload definition
        :rtype: str
        """

        lp = len(self._payload)
        if mode == nmt.GET:
            if lp == 1 and self._payload[0] == "OK":
                key = "QTMACK"
            elif lp == 2 and self._payload[0] == "ERROR":
                key = "QTMNAK"
        return key

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
        if self._defsource == nmt.DEF_UNKN:
            stg += ", NOMINAL"
        for att, val in self.__dict__.items():
            if att[0] != "_":  # only show public attributes
                stg += f", {att}={val}"
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

        output = f"${self._talker}{self._msgID}"
        for att in self._payload:
            output += "," + att
        output += f"*{self._checksum}\r\n"
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
        if att in (nmt.CH, nmt.ST, nmt.LAD, nmt.LND, nmt.QS):
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

        if att in (nmt.CH, nmt.ST, nmt.LAD, nmt.LND, nmt.QS):
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
            if isinstance(val, str):
                vals = str(val.replace(":", ""))
            else:  # time
                vals = time2str(val)
        elif att == nmt.DT:
            if isinstance(val, str):
                # yyyymmdd -> ddmmyy
                val = val.replace("-", "")
                vals = f"{val[6:8]}{val[4:6]}{val[2:4]}"
            else:  # datetime
                vals = date2str(val, att)
        elif att == nmt.DTL:
            # yyyymmdd -> ddmmyyyy
            if isinstance(val, str):
                val = val.replace("-", "")
                vals = f"{val[6:8]}{val[4:6]}{val[0:4]}"
            else:  # datetime
                vals = date2str(val, att)
        elif att == nmt.DM:
            # yyyymmdd -> mmddyy
            if isinstance(val, str):
                val = val.replace("-", "")
                vals = f"{val[4:6]}{val[6:8]}{val[2:4]}"
            else:  # datetime
                vals = date2str(val, att)
        else:
            raise nme.NMEATypeError(f"Unknown attribute type {att}.")
        return vals

    @staticmethod
    def nomval(att: str, msgmode: int = nmt.GET) -> object:
        """
        Return nominal value for specified attribute type

        :param str att: attribute type e.g. 'DE'
        :param int msgmode: message mode GET/SET/POLL
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
        elif att == nmt.QS:  # Quectel status attribute
            if msgmode == nmt.POLL:
                val = "R"  # read
            elif msgmode == nmt.SET:
                val = "W"  # write
            else:
                val = "OK"  # acknowledgement
        else:
            raise nme.NMEATypeError(f"Unknown attribute type {att}.")
        return val
