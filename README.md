pynmeagps
=========

`pynmeagps` is an original lightweight Python library aimed *primarily* at the subset of the NMEA 0183 protocol relevant to GNSS/GPS receivers - that is, NMEA 0183 'talkers' 'Gx' (standard) or 'Px' (proprietary).

The intention is to make it as easy as possible to read, parse and utilise NMEA GNSS/GPS messages in Python applications. 

The `pynmeagps` homepage is located at [http://github.com/semuconsulting/pynmeagps](http://github.com/semuconsulting/pynmeagps).

**FYI** There is a companion library [pyubx2](http://github.com/semuconsulting/pyubx2), which handles u-blox UBX protocol GNSS/GPS messages.

---

### Current Status

![Status](https://img.shields.io/pypi/status/pynmeagps)
![Release](https://img.shields.io/github/v/release/semuconsulting/pynmeagps?include_prereleases)
![Build](https://img.shields.io/github/workflow/status/semuconsulting/pynmeagps/pynmeagps)
![Codecov](https://img.shields.io/codecov/c/github/semuconsulting/pynmeagps)
![Release Date](https://img.shields.io/github/release-date-pre/semuconsulting/pynmeagps)
![Last Commit](https://img.shields.io/github/last-commit/semuconsulting/pynmeagps)
![Contributors](https://img.shields.io/github/contributors/semuconsulting/pynmeagps.svg)
![Open Issues](https://img.shields.io/github/issues-raw/semuconsulting/pynmeagps)

At time of writing the library implements a comprehensive set of GNSS NMEA messages relating to GNSS/GPS devices, but is readily [extensible](#extensibility). Refer to `NMEA_MSGIDS` in [nmeatypes_core.py](https://github.com/semuconsulting/pynmeagps/blob/master/pynmeagps/nmeatypes_core.py) for the complete dictionary of messages currently supported. Additional NMEA 'talkers' may be added in due course.

Sphinx API Documentation in HTML format is available at [http://semuconsulting.com/pynmeagps](http://semuconsulting.com/pynmeagps).

Contributions welcome - please refer to [CONTRIBUTING.MD](https://github.com/semuconsulting/pynmeagps/blob/master/CONTRIBUTING.md).

[Bug reports](https://github.com/semuconsulting/pynmeagps/blob/master/.github/ISSUE_TEMPLATE/bug_report.md) and [Feature requests](https://github.com/semuconsulting/pynmeagps/blob/master/.github/ISSUE_TEMPLATE/feature_request.md) - please use the templates provided.

---

## <a name="installation">Installation</a>

`pynmeagps` is compatible with Python 3.6+ and has no third-party library dependencies.

In the following, `python` & `pip` refer to the python3 executables. You may need to type 
`python3` or `pip3`, depending on your particular environment.

![Python version](https://img.shields.io/pypi/pyversions/pynmeagps.svg?style=flat)
[![PyPI version](https://img.shields.io/pypi/v/pynmeagps.svg?style=flat)](https://pypi.org/project/pynmeagps/)
![PyPI downloads](https://img.shields.io/pypi/dm/pynmeagps.svg?style=flat)

The recommended way to install the latest version of `pynmeagps` is with
[pip](http://pypi.python.org/pypi/pip/):

```shell
python -m pip install --upgrade pynmeagps
```

If required, `pynmeagps` can also be installed using virtualenv, e.g.:

```shell
python -m pip install --user --upgrade virtualenv
python -m virtualenv env
source env/bin/activate (or env\Scripts\activate on Windows)
(env) python -m pip install --upgrade pynmeagps
...
deactivate
```

---

## Reading (Streaming)

You can create an `NMEAReader` object by calling the constructor with an active stream object. 
The stream object can be any data stream which supports a `read(n) -> bytes` method (e.g. File or Serial, with 
or without a buffer wrapper).

Individual input NMEA messages can then be read using the `NMEAReader.read()` function, which returns both the raw data (as bytes) and the parsed data (as an `NMEAMessage` object). The function is thread-safe in so far as the incoming data stream object is thread-safe. `NMEAReader` also implements an iterator.

The `NMEAReader` constructor includes an optional `nmea_only` flag which governs behaviour if the stream includes non-NMEA data (e.g. proprietary UBX or Garmin data). If set to 'False' (the default), it will ignore such data and continue with the next valid NMEA message. If set to 'True', it will raise a `NMEAStreamError`. **NB:** if the `nmea_only` flag is set to 'False', the `NMEAReader.read()` function will block until it receives a NMEA message (or the input stream times out).

Examples:

* Serial input - this example will ignore any non-NMEA data.

```python
>>> from serial import Serial
>>> from pynmeagps import NMEAReader
>>> stream = Serial('/dev/tty.usbmodem14101', 9600, timeout=3)
>>> nmr = NMEAReader(stream)
>>> (raw_data, parsed_data) = nmr.read()
```

* File input (using iterator) - this example will produce a `NMEAStreamError` if non-NMEA data is encountered.

```python
>>> from pynmeagps import NMEAReader
>>> stream = open('nmeadata.log', 'rb')
>>> nmr = MEAReader(stream, True)
>>> for (raw_data, parsed_data) in nmr: print(parsed_data)
...
```

## Parsing

You can parse individual NMEA messages using the static `NMEAReader.parse(data, validate=1)` function, which takes a string or bytes containing an NMEA message and returns a `NMEAMessage` object.

The validate flag signifies whether to validate the incoming checksum (1), msgid (2), both (3) or neither (0). If invalid, a `NMEAParseError` will be raised. The default (1) is to validate the checksum but ignore (and discard) an unknown msgID.

Example:

```python
>>> from pynmeagps import NMEAReader
>>> msg = NMEAReader.parse('$GNGLL,5327.04319,S,00214.41396,E,223232.00,A,A*68\r\n', 1)
>>> print(msg)
<NMEA(GNGLL, lat=-53.45072, NS=S, lon=2.240233, EW=E, time=22:32:32, status=A, posMode=A)>
```

The `NMEAMessage` object exposes different public properties depending on its message ID,
e.g. the `RMC` message has the following properties:

```python
>>> print(msg)
<NMEA(GNRMC, time=22:18:38, status=A, lat=52.62063, NS=N, lon=-2.16012, EW=W, spd=37.84, cog=, date=2021-03-05, mv=, mvEW=, posMode=A)>
>>> msg.msgID
'RMC'
>>> msg.lat, msg.lon
(52.62063, -2.16012)
>>> msg.spd
37.84
```

## Generating

You can create an `NMEAMessage` object by calling the constructor with the following parameters:
1. talker (must be a valid talker from `pynmeagps.NMEA_TALKERS`, or blank for proprietary messages)
1. message id (must be a valid id from `pynmeagps.NMEA_MSGIDS`)
2. mode (0=GET, 1=SET, 2=POLL)
3. (optional) a series of keyword parameters representing the message payload

The 'mode' parameter signifies whether the message payload refers to a:

* GET message (i.e. output from the receiver - NB these would normally be generated via the NMEAReader.read() or NMEAReader.parse() methods but can also be created manually)
* SET message (i.e. command input to the receiver)
* POLL message (i.e. query input to the receiver in anticipation of a response back)

The message payload can be defined via keyword parameters in one of three ways:
1. A single keyword parameter of `payload` containing the full payload as a list of string values (any other keyword parameters will be ignored).
2. One or more keyword parameters corresponding to individual message attributes. Any attributes not explicitly provided as keyword
parameters will be set to a nominal value according to their type.
3. If no keyword parameters are passed, the payload is assumed to be null.

e.g. to generate a GNGPQ POLL message:

```python
>>> from pynmeagps import NMEAMessage, POLL
>>> msg = NMEAMessage('GN','GPQ', POLL, msgId='GGA')
>>> print(msg)
<NMEA(GNGPQ, msgId=GGA)>
```

**NB:** Once instantiated, an `NMEAMessage` object is immutable.

### Serializing

The `NMEAMessage` class implements a `serialize()` method to convert a `NMEAMessage` object to a bytes array suitable for writing to an output stream.

```python
>>> from pynmeagps import NMEAMessage, POLL
>>> msg = NMEAMessage('GN','GPQ', POLL, msgId='GGA')
>>> msg.serialize()
b'$GNGPQ,GGA*22\r\n'
```

---

## Examples

The following examples can be found in the `\examples` folder:

1. `nmeadump.py` is a simple command line utility to stream the parsed NMEA output of a GNSS/GPS device on a specified port.

1. `nmeastreamer.py` illustrates how to implement a threaded serial reader for NMEA messages using pynmeagps.NMEAReader. 

1. `nmeafile.py` illustrates how to implement a binary file reader for UBX messages using the pynmeagps.NMEAReader iterator function. 

1. `gpxtracker.py` illustrates a simple CLI tool to convert a binary NMEA data dump to a `*.gpx` track file using pynmeagps.NMEAReader.

## <a name="extensibility">Extensibility</a>

The UBX protocol is principally defined in the modules `nmeatypes_*.py` as a series of dictionaries. Additional message types 
can be readily added to the appropriate dictionary. Message payload definitions must conform to the following rules:

```
1. attribute names must be unique within each message class
2. attribute types must be one of the valid types (IN, DE, CH, etc.)
3. repeating groups must be defined as a tuple ('numr', {dict}), where:
   'numr' is either:
     a. an integer representing a fixed number of repeats e.g. 32
     b. a string representing the name of a preceding attribute containing the number of repeats e.g. 'numSv'
     c. 'None' for an indeterminate repeating group. Only one such group is permitted per payload and it must be at the end.
   {dict} is the nested dictionary of repeating items
```

---

## Graphical Client

A python/tkinter graphical GPS client which supports both NMEA and UBX protocols is available at: 

[http://github.com/semuconsulting/PyGPSClient](http://github.com/semuconsulting/PyGPSClient)

---

## Author Information

![License](https://img.shields.io/github/license/semuconsulting/pynmeagps.svg)

semuadmin@semuconsulting.com
