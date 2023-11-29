# pynmeagps Release Notes

### RELEASE CANDIDATE 1.0.32

ENHANCEMENTS:

1. Cater for NMEA streams with LF (b"\x0a") rather than CRLF (b"\x0d\x0a") message terminators.

### RELEASE 1.0.31

ENHANCEMENTS:

1. Extend `NMEA_HDR` to include *all* known Talker IDs (*not just those relevant to GNSS*).
2. Minor Internal streamlining.

### RELEASE 1.0.30

ENHANCEMENTS:

1. Cater for 'IN' (Integrated Navigation) Talker ID.

### RELEASE 1.0.29

ENHANCEMENTS:

1. Cater for legacy "BD" (Beidou) NMEA Talker ID.

### RELEASE 1.0.28

ENHANCEMENTS:

1. Add 'NAVIC' to list of gnssId enumerations - reference only, no functional change.

### RELEASE 1.0.27

CHANGES:

1. Add write capability to socket_stream wrapper, allowing clients to write to NMEAReader socket stream (NMEAReader.datastream) as well as read from it.
1. Update constructor arguments and docstrings to clarify API (no functional changes).

### RELEASE 1.0.26

CHANGES:

1. Deprecated `NMEAReader.iterate()` method removed - use the standard iterator instead e.g. `nmr = NMEAReader(stream, **wkargs): for (raw,parse) in nmr: ...`, passing any `quitonerror` or `errorhandler` kwargs to the NMEAReader constructor.
1. Internal streamlining of helper methods.

### RELEASE 1.0.25

FIXES:

1. Add support for non-standard 3-digit degree latitude value, e.g.
   `'$GNGLL,02348.3822990,S,15313.5862807,E,040856.82,A,D*5F'`
1. NB: footprint of `dmm2ddd` helper method has changed - `att` argument no longer required.
1. Fixes #37

### RELEASE 1.0.24

1. Remove Python 3.7 from workflows.
1. Add proprietary POLL messages to nmeatypes_poll.py

### RELEASE 1.0.23

ENHANCEMENTS:

1. Add proprietary Trimble message definitions.
    - GMP   GNSS Map Projection Fix Data
    - LLQ 	Leica local position and quality
    - ROT 	Rate of turn
    - PASHR,ALR Alarms
    - PASHR,ARA True Heading
    - PASHR,ARR Vector & Accuracy
    - PASHR,ATT True Heading
    - PASHR,BTS Bluetooth Status
    - PASHR,CAP Parameters of Antenna Used at Received Base
    - PASHR,CPA Height of Antenna Used at Received Base
    - PASHR,CPO Position of Received Base
    - PASHR,DDM Differential Decoder Message
    - PASHR,DDS Differential Decoder Status
    - PASHR,HPR True Heading
    - PASHRHR Proprietary Roll and Pitch
    - PASHR,LTN Latency
    - PASHR,MDM Modem State and Parameter
    - PASHR,PBN Position and Velocity Information
    - PASHR,POS Position
    - PASHR,PTT PPS Time Tag
    - PASHR,PWR Power Status
    - PASHR,RCS Recording Status
    - PASHR,SBD BEIDOU Satellites Status
    - PASHR,SGA GALILEO Satellites Status (E1,E5a,E5b)
    - PASHR,SGL GLONASS Satellites Status
    - PASHR,SGO GALILEO Satellites Status (E1,E5a,E5b,E6)
    - PASHR,SGP GPS Satellites Status
    - PASHR,SIR IRNSS Satellites Status
    - PASHR,SLB L-Band Satellites Status
    - PASHR,SQZ QZSS Satellites Status
    - PASHR,SSB SBAS Satellites Status
    - PASHR,TEM Receiver Temperature
    - PASHR,THS True Heading and Status
    - PASHR,TTT Event Marker
    - PASHR,VCR Vector and Accuracy
    - PASHR,VCT Vector and Accuracy
    - PASHR,VEL Velocity
    - FUGDP Fugro Dynamic Positioning
    - GPPADV,110 Position and satellite information for RTK network operations 110
    - GPPADV,120 Position and satellite information for RTK network operations 120
    - PTNL,AVR 	Time, yaw, tilt, range, mode, PDOP, and number of SVs for Moving Baseline RTK
    - PTNL,BPQ 	Base station position and position quality indicator
    - PTNL,DG 	L-band corrections and beacon signal strength and related information
    - PTNL,EVT 	Event marker data
    - PTNL,GGK 	Time, position, position type, and DOP values
    - PTNL,PJK 	Time, position, position type, and DOP values
    - PTNL,PJT 	Projection type
    - PTNL,REX Rover Extended Output
    - PTNL,VGK 	Time, locator vector, type, and DOP values
    - PTNL,VHD 	Heading Information

### RELEASE 1.0.22

FIXES:

1. Rounding removed from `haversine` helper method.

### RELEASE 1.0.21

ENHANCEMENTS:

1. Add `bearing` helper method.

### RELEASE 1.0.20

CHANGES:

1. `quitonerror` and `errorhandler` kwargs added to NMEAReader constructor - see Sphinx documentation for details.
2. `NMEAReader.iterate()` method deprecated - use the standard iterator instead e.g. `nmr = NMEAReader(stream, **wkargs): for (raw,parse) in nmr: ...`, passing any `quitonerror` or `errorhandler` kwargs to the NMEAReader constructor.

### RELEASE 1.0.19

FIXES:

1. Fix typo in PUBX00 payload definition - PDOP is now TDOP. Thanks to @dbstf for issue report.
1. Fix handling of VALMSGID flag in NMEAReader. Thanks to @nmichaels-qualinx for issue report.

### RELEASE 1.0.18

ENHANCEMENTS:

1. Following utility methods added to nmeahelpers.py:

- `latlon2dms` - converts decimal lat/lon to degrees, minutes, decimal seconds format e.g. "53°20′45.6″N", "2°32′46.68″W"
- `latlon2dmm` - converts decimal lat/lon to degrees, decimal minutes format e.g. "53°20.76′N", "2°32.778′W"
- `llh2iso6709` - converts lat/lon and altitude (hMSL) to ISO6709 format e.g. "+27.5916+086.5640+8850CRSWGS_84/"
- `ecef2llh` - converts ECEF (X, Y, Z) coordinates to geodetic (lat, lon, ellipsoidal height) coordinates
- `llh2ecef` - converts geodetic (lat, lon, ellipsoidal height) coordinates to ECEF (X, Y, Z) coordinates
- `haversine` - finds spherical distance in km between two sets of (lat, lon) coordinates


### RELEASE 1.0.17

CHANGES:

1. shields.io build status badge URL updated.

No other functional changes.

### RELEASE 1.0.16

ENHANCEMENTS:

1. `time2utc` helper method enhanced to cater for proprietary NMEA messages containing timestamps in format hh.mm.ss rather than hh.mm.ss.ss (i.e. missing decimal seconds). Addresses PR #19.

### RELEASE 1.0.15

ENHANCEMENTS:

1. Enhancement to NMEAMessage constructor - will now automatically derive value of `NS` or `EW` attributes from provided lat/lon e.g. `lon` < 0 => `EW` = "W"
2. Enhancement to NMEAMessage constructor - optional keyword argument `hpnmeamode` added which allows NMEA position
message payloads to be constructed to 7dp decimal minutes rather than the standard 5dp (i.e. (d)ddmm.mmmmmmm rather than (d)ddmm.mmmm). **NB:** this is primarily for manually constructed messages. Messages parsed from a GNSS receiver data stream retain whatever level of precision is output by the receiver to a maximum 10dp of decimal degrees.

### RELEASE 1.0.14

CHANGES:

1. `nmeadump` CLI utility has been removed and replaced by the `gnssdump` utility available via the `pygnssutils` PyPi package.
2. Python 3.11 classifier added to setup.

### RELEASE 1.0.13.

FIXES:

1. When manually creating NMEA Messages, the nominal (default) value of time and date fields is now set to UTC time rather than local time. This is relevant, for example, when constructing NMEA GGA messages to send to NTRIP casters.

### RELEASE 1.0.12

CHANGES:

1. Add support for THS message type.
1. Extend test coverage for socket handler.

### RELEASE 1.0.11

ENHANCEMENTS:

1. Add capability to read from TCP/UDP socket as well as serial stream. Utilises a SocketStream utility class to allow sockets to be read using standard stream-like read(bytes) and readline() methods.


### RELEASE 1.0.10

FIXES:

1. GBS and GSA message definitions updated - `systemId` and `signalId` now correctly defined as HX rather than IN.

### RELEASE 1.0.9

FIXES:

1. GRS message definition updated - `systemId` and `signalId` now correctly defined as HX rather than IN.

### RELEASE 1.0.8

ENHANCEMENTS:

1. `identity` property added to NMEAMessage for consistency with companion `pyubx2` library - identity = (talker+msgID)
2. internal refactoring of error handling in `NMEAReader.read()` method to make it more consistent with `pyubx2` when processing corrupted data streams.

### RELEASE 1.0.7

FIXES:

1. HX attribute type processing corrected - will now parse HX values as hex strings rather than convert to/from integers.
2. GSV payload corrected - SignalId is now hex.

### RELEASE 1.0.6

ENHANCEMENTS:

1. Python 3.10 compatibility added
2. Minor pylint code tweaks

### RELEASE 1.0.5

ENHANCEMENTS:

1. Filter added to `nmeadump` cli utility to limit output to specified NMEA msgIDs. See README for usage.
2. Update `dmm2ddd()` helper method to increase conversion accuracy from 6 to 8 decimal places - thanks for Doradx for the contribution.

### RELEASE 1.0.4

ENHANCEMENTS:

1. The nmeadump.py example has been moved into the pynmeagpscli module and configured as a setup entry point. It is now available as a simple command line utility. See README for usage.

### RELEASE 1.0.3

FIXES:

1. Fixed diffAge field type in GGA payload definition.

### RELEASE 1.0.2

FIXES:

1. Fixed typo in VTG payload definition - `cogT` is now `cogt`. Test script updated.

### RELEASE 1.0.1

FIXES:

1. Fixed typo in GBS payload definition - `effLon` is now `errLon`. Test script updated.
2. Fixed cosmetic typo in nmeafile.py example - functionality not affected.

### RELEASE 1.0.0

CHANGES:

1. Marked to v1.0.0 Production/Stable. No other functional changes.

### RELEASE 0.1.8-beta

FIXES:

1. NMEA PUBX msgId parsed as str rather than int.

ENHANCEMENTS:

2. nmeatypes_core.py NMEA_MSGID table split into standard and proprietary dicts. 
3. nmeapollall.py example added.

### RELEASE 0.1.7-beta

ENHANCEMENTS:

1. Following standard message types added: AAM, APA, APB, BOD, BWC, MSK, MSS, RMA, RMB, STN, VBW, WPL, XTE, 
2. Following proprietary message types added: (Garmin) GRME, GRMM, GRMZ

Further types will be added in subsequent releases. Shout or submit PR if you want yours prioritised.

### RELEASE 0.1.6-beta

ENHANCEMENTS:

1. message types HDG, HDM, HDT, RTE added
2. msgdesc() helper method added to get description of NMEA message type.
3. construction of proprietary messages (talker = 'P') made more consistent with standard messages.

FIXES:

1. nominal value for HX (hex) attribute type updated to integer rather than string (only currently affects RLM message type).


### RELEASE 0.1.5-beta

CHANGES:

1. Optional arguments to NMEARreader constructor and parse() method have been changed to **kwargs rather than args for future flexibility. See docstrings for usage.

### RELEASE 0.1.4-beta

ENHANCEMENTS:

1. Add Garmin proprietary NMEA sentences GET and SET.

### RELEASE 0.1.3-beta

ENHANCEMENTS:

1. Parse validate flag added to NMEAReader.read() method, defaults to VLCKSUM (1 - check checksum only); other options are VALNONE = 0, 
VALMSGID = 2. Options can be ANDed. Examples updated accordingly.

### RELEASE 0.1.2-beta

1. Constructor enhanced to allow NMEAMessage to be created using typed values.

### RELEASE 0.1.1-beta

1. README.MD and GitHub workflow/coverage updated

### RELEASE 0.1.0-beta

1. Initial public beta release
