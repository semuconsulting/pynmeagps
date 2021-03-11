# pynmeagps Release Notes

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