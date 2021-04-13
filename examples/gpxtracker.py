"""
Simple CLI utility which creates a GPX track file
from a binary NMEA dump.

Dump must contain NMEA GGA messages.

There are a number of free online GPX viewers
e.g. https://gpx-viewer.com/view

Could have used minidom for XML but didn't seem worth it.

Created on 7 Mar 2021

@author: semuadmin
"""

import os
from datetime import datetime
from time import strftime
from pynmeagps.nmeareader import NMEAReader
import pynmeagps.exceptions as nme

XML_HDR = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'

GPX_NS = " ".join(
    (
        'xmlns="http://www.topografix.com/GPX/1/1"',
        'creator="pynmeagps" version="1.1"',
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',
        'xsi:schemaLocation="http://www.topografix.com/GPX/1/1',
        'http://www.topografix.com/GPX/1/1/gpx.xsd"',
    )
)
GITHUB_LINK = "https://github.com/semuconsulting/pynmeagps"


class NMEATracker:
    """
    NMEATracker class.
    """

    def __init__(self, infile, outdir):
        """
        Constructor.
        """

        self._filename = infile
        self._outdir = outdir
        self._infile = None
        self._trkfname = None
        self._trkfile = None
        self._nmeareader = None
        self._connected = False

    def open(self):
        """
        Open datalog file.
        """

        self._infile = open(self._filename, "rb")
        self._connected = True

    def close(self):
        """
        Close datalog file.
        """

        if self._connected and self._infile:
            self._infile.close()

    def reader(self, validate=False):
        """
        Reads and parses UBX message data from stream
        using UBXReader iterator method
        """

        i = 0
        self._nmeareader = NMEAReader(self._infile, validate=validate)

        self.write_gpx_hdr()

        for (_, msg) in self._nmeareader:  # invokes iterator method
            try:
                if msg.msgID == "GGA":
                    dat = datetime.now()
                    tim = msg.time
                    dat = (
                        dat.replace(
                            year=dat.year,
                            month=dat.month,
                            day=dat.day,
                            hour=tim.hour,
                            minute=tim.minute,
                            second=tim.second,
                        ).isoformat()
                        + "Z"
                    )
                    if msg.quality == 1:
                        fix = "3d"
                    elif msg.quality == 2:
                        fix = "2d"
                    else:
                        fix = "none"
                    self.write_gpx_trkpnt(
                        msg.lat,
                        msg.lon,
                        ele=msg.alt,
                        time=dat,
                        fix=fix,
                        hdop=msg.HDOP,
                    )
                    i += 1
            except (nme.NMEAMessageError, nme.NMEATypeError, nme.NMEAParseError) as err:
                print(f"Something went wrong {err}")
                continue

        self.write_gpx_tlr()

        print(f"\n{i} GGA message{'' if i == 1 else 's'} read from {self._filename}")
        print(f"{i} trackpoint{'' if i == 1 else 's'} written to {self._trkfname}")

    def write_gpx_hdr(self):
        """
        Open gpx file and write GPX track header tags
        """

        timestamp = strftime("%Y%m%d%H%M%S")
        self._trkfname = os.path.join(self._outdir, f"gpxtrack-{timestamp}.gpx")
        self._trkfile = open(self._trkfname, "a")

        date = datetime.now().isoformat() + "Z"
        gpxtrack = (
            XML_HDR + "<gpx " + GPX_NS + ">"
            f"<metadata>"
            f'<link href="{GITHUB_LINK}"><text>pynmeagps</text></link><time>{date}</time>'
            "</metadata>"
            "<trk><name>GPX track from NMEA datalog</name><trkseg>"
        )

        self._trkfile.write(gpxtrack)

    def write_gpx_trkpnt(self, lat: float, lon: float, **kwargs):
        """
        Write GPX track point from NAV-PVT message content
        """

        trkpnt = f'<trkpt lat="{lat}" lon="{lon}">'

        # these are the permissible elements in the GPX schema for wptType
        # http://www.topografix.com/GPX/1/1/#type_wptType
        for tag in (
            "ele",
            "time",
            "magvar",
            "geoidheight",
            "name",
            "cmt",
            "desc",
            "src",
            "link",
            "sym",
            "type",
            "fix",
            "sat",
            "hdop",
            "vdop",
            "pdop",
            "ageofdgpsdata",
            "dgpsid",
            "extensions",
        ):
            if tag in kwargs:
                val = kwargs[tag]
                trkpnt += f"<{tag}>{val}</{tag}>"

        trkpnt += "</trkpt>"

        self._trkfile.write(trkpnt)

    def write_gpx_tlr(self):
        """
        Write GPX track trailer tags and close file
        """

        gpxtrack = "</trkseg></trk></gpx>"
        self._trkfile.write(gpxtrack)
        self._trkfile.close()


if __name__ == "__main__":

    print("NMEA datalog to GPX file converter\n")
    infilep = input("Enter input NMEA datalog file: ").strip('"')
    outdirp = input("Enter output directory: ").strip('"')
    #     infilep = "C:\\Users\\username\\Downloads\\pygpsdata-test.log"
    #     outdirp = "C:\\Users\\username\\Downloads"
    tkr = NMEATracker(infilep, outdirp)
    print(f"\nProcessing file {infilep}...")
    tkr.open()
    tkr.reader()
    tkr.close()
    print("\nOperation Complete")
