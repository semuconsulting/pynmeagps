pynmeagps
=========

`pynmeagps` is an original Python library aimed *primarily* at the subset of the NMEA 0183 &copy; v4 protocol relevant to GNSS/GPS receivers - that is, NMEA 0183 'talkers' 'Gx' (standard) or 'Px' (proprietary).

The intention is to make it as easy as possible to read, parse and utilise NMEA GNSS/GPS messages in Python applications. 

The `pynmeagps` homepage is located at [https://github.com/semuconsulting/pynmeagps](https://github.com/semuconsulting/pynmeagps).

**FYI** There is a companion library [pyubx2](http://github.com/semuconsulting/pyubx2), which handles u-blox &trade; UBX &copy; protocol GNSS/GPS messages.

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

At time of writing the library implements a comprehensive set of outbound (GET) and inbound (SET/POLL) GNSS NMEA messages relating to GNSS/GPS devices, but is readily [extensible](#extensibility). Refer to `NMEA_MSGIDS` and `NMEA_MSGIDS_PROP` in [nmeatypes_core.py](https://github.com/semuconsulting/pynmeagps/blob/master/pynmeagps/nmeatypes_core.py) for the complete dictionary of messages currently supported. Additional NMEA 'talkers' may be added in due course. While the NMEA 0183 protocol itself is proprietary, the definitions here have been collated from public domain sources.

Sphinx API Documentation in HTML format is available at [https://www.semuconsulting.com/pynmeagps](https://www.semuconsulting.com/pynmeagps).

Contributions welcome, particularly any standard or proprietary NMEA message definitions not yet included - please refer to [CONTRIBUTING.MD](https://github.com/semuconsulting/pynmeagps/blob/master/CONTRIBUTING.md).

[Bug reports](https://github.com/semuconsulting/pynmeagps/blob/master/.github/ISSUE_TEMPLATE/bug_report.md) and [Feature requests](https://github.com/semuconsulting/pynmeagps/blob/master/.github/ISSUE_TEMPLATE/feature_request.md) - please use the templates provided.

---

## <a name="installation">Installation</a>

`pynmeagps` is compatible with Python 3.6+ and has no third-party library dependencies.

In the following, `python` & `pip` refer to the Python 3 executables. You may need to type 
`python3` or `pip3`, depending on your particular environment.

![Python version](https://img.shields.io/pypi/pyversions/pynmeagps.svg?style=flat)
[![PyPI version](https://img.shields.io/pypi/v/pynmeagps.svg?style=flat)](https://pypi.org/project/pynmeagps/)
![PyPI downloads](https://img.shields.io/pypi/dm/pynmeagps.svg?style=flat)

The recommended way to install the latest version of `pynmeagps` is with
[pip](http://pypi.python.org/pypi/pip/):

```shell
python -m pip install --upgrade pynmeagps
```

If required, `pynmeagps` can also be installed into a virtual environment, e.g.:

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

```
class pynmeagps.nmeareader.NMEAReader(stream, **kwargs)
```

You can create an `NMEAReader` object by calling the constructor with an active stream object. 
The stream object can be any data stream which supports a `read(n) -> bytes` method (e.g. File or Serial, with 
or without a buffer wrapper).

Individual input NMEA messages can then be read using the `NMEAReader.read()` function, which returns both the raw data (as bytes) and the parsed data (as an `NMEAMessage` object, via the `parse()` method). The function is thread-safe in so far as the incoming data stream object is thread-safe. `NMEAReader` also implements an iterator.

The constructor accepts the following optional keyword arguments:


* `nmeaonly`: True = raise error if stream contains non-NMEA data, False = ignore non-NMEA data (default)
* `validate`: bitfield validation flags (can be used in combination):
- `VALCKSUM` (0x01) = validate checksum (default)
- `VALMSGID` (0x02) = validate msgId (i.e. raise error if unknown NMEA message is received)
* `msgmode`: 0 = GET (default), 1 = SET, 2 = POLL


Examples:

* Serial input - this example will ignore any non-NMEA data.

```python
>>> from serial import Serial
>>> from pynmeagps import NMEAReader
>>> stream = Serial('/dev/tty.usbmodem14101', 9600, timeout=3)
>>> nmr = NMEAReader(stream)
>>> (raw_data, parsed_data) = nmr.read()
>>> print(parsed_data)
```

* File input (using iterator) - this example will produce a `NMEAStreamError` if non-NMEA data is encountered.

```python
>>> from pynmeagps import NMEAReader
>>> stream = open('nmeadata.log', 'rb')
>>> nmr = NMEAReader(stream, nmeaonly=True)
>>> for (raw_data, parsed_data) in nmr: print(parsed_data)
...
```

## Parsing

You can parse individual NMEA messages using the static `NMEAReader.parse(message)` function, which takes a string or bytes containing an NMEA message and returns an `NMEAMessage` object.

Note that latitude and longitude are parsed as signed decimal values for ease of use. Helper methods `deg2dms` and `deg2dmm` are available to convert decimal degrees to d°m′s.s″ or d°m.m′ display format.

Attributes within repeating groups are parsed with a two-digit suffix (svid_01, svid_02, etc.).

The `parse()` function accepts the following optional keyword arguments:

* `validate`: bitfield validation flags (can be used in combination):
- `VALCKSUM` (0x01) = validate checksum (default)
- `VALMSGID` (0x02) = validate msgId (i.e. raise error if unknown NMEA message is received)
* `msgmode`: 0 = GET (default), 1 = SET, 2 = POLL

Example:

```python
>>> from pynmeagps import NMEAReader
>>> msg = NMEAReader.parse('$GNGLL,5327.04319,S,00214.41396,E,223232.00,A,A*68\r\n')
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

```
class pynmeagps.nmeamessage.NMEAMessage(talker: str, msgID: str, msgmode: int, **kwargs)
```

You can create an `NMEAMessage` object by calling the constructor with the following parameters:
1. talker (must be a valid talker from `pynmeagps.NMEA_TALKERS`)
1. message id (must be a valid id from `pynmeagps.NMEA_MSGIDS` or `pynmeagps.NMEA_MSGIDS_PROP`)
2. msgmode (0=GET, 1=SET, 2=POLL)
3. (optional) a series of keyword parameters representing the message payload

The 'msgmode' parameter signifies whether the message payload refers to a:

* GET message (i.e. output from the receiver - NB these would normally be generated via the NMEAReader.read() or NMEAReader.parse() methods but can also be created manually)
* SET message (i.e. command input to the receiver)
* POLL message (i.e. query input to the receiver in anticipation of a response back)

The message payload can be defined via keyword arguments in one of two ways:
1. A single keyword parameter of `payload` containing the full payload as a list of string values (any other keyword parameters will be ignored).
2. One or more keyword parameters corresponding to individual message attributes. Any attributes not explicitly provided as keyword
parameters will be set to a nominal value according to their type.

e.g. Create a GLL message, passing the entire payload as a list of strings in native NMEA format:

```python
>>> from pynmeagps import NMEAMessage, GET
>>> pyld=['4330.00000','N','00245.000000','W','120425.234','A','A']
>>> msg = NMEAMessage('GN', 'GLL', GET, payload=pyld)
print(msg)
<NMEA(GNGLL, lat=43.5, NS=N, lon=-2.75, EW=W, time=12:04:25.234000, status=A, posMode=A)>
```

e.g. Create GLL (GET) and GNQ (POLL) message, passing individual typed values as keywords, with any omitted keywords defaulting to nominal values (in the GLL example, the 'time' parameter has been omitted and has defaulted to the current time):

```python
>>> from pynmeagps import NMEAMessage, GET
>>> msg = NMEAMessage('GN', 'GLL', GET, lat=43.5, NS='N', lon=2.75, EW='W', status='A', posMode='A')
>>> print(msg)
<NMEA(GNGLL, lat=43.5, NS='N', lon=-2.75, EW='W', time='12:04:25.234745', status='A', posMode='A')>
```

```python
>>> from pynmeagps import NMEAMessage, POLL
>>> msg = NMEAMessage('EI', 'GNQ', POLL, msgId='RMC')
>>> print(msg)
<NMEA(EIGNQ, msgId=RMC)>
```

**NB:** Once instantiated, an `NMEAMessage` object is immutable.

### Serializing

The `NMEAMessage` class implements a `serialize()` method to convert an `NMEAMessage` object to a bytes array suitable for writing to an output stream.

```python
>>> from serial import Serial
>>> from pynmeagps import NMEAMessage, POLL
>>> stream = Serial('COM6', 38400, timeout=3)
>>> msg = NMEAMessage('EI','GNQ', POLL, msgId='RMC')
>>> msg.serialize()
b'$EIGNQ,RMC*24\r\n'
>>> stream.write(msg.serialize())
```

---

## Examples

The following examples can be found in the `\examples` folder:

1. `nmeastreamer.py` illustrates how to implement a threaded serial reader for NMEA messages using pynmeagps.NMEAReader, and send poll requests for specific NMEA message types. 

1. `nmeafile.py` illustrates how to implement a binary file reader for NMEA messages using the pynmeagps.NMEAReader iterator function. 

1. `gpxtracker.py` illustrates a simple CLI tool to convert an NMEA data dump to a `*.gpx` track file using pynmeagps.NMEAReader.

1. `/webserver/gpsstreamer.py` illustrates a simple HTTP web server wrapper around a threaded pynmeagps streaming and parsing service. To use, cd to the `/examples/webserver` folder, execute the `gpsstreamer.py` module and direct your browser to http://localhost:8080. The web page will update dynamically every 5 seconds. You can also access the parsed NMEA data directly via the REST API http://localhost:8080/gps.

## <a name="extensibility">Extensibility</a>

The NMEA protocol is principally defined in the modules `nmeatypes_*.py` as a series of dictionaries. Additional message types 
can be readily added to the appropriate dictionary. Message payload definitions must conform to the following rules:

```
1. attribute names must be unique within each message class
2. avoid reserved names 'msgID', 'talker', 'payload', 'checksum'.
3. attribute types must be one of the valid types (IN, DE, CH, etc.)
4. repeating groups must be defined as a tuple ('numr', {dict}), where:
   'numr' is either:
     a. an integer representing a fixed number of repeats e.g. 32
     b. a string representing the name of a preceding attribute containing the number of repeats e.g. 'numSv'
     c. 'None' for an indeterminate repeating group. Only one such group is permitted per payload and it must be at the end.
   {dict} is the nested dictionary of repeating items
```

---

## <a name="cli">Command Line Utility</a>

If `pynmeagps` is installed using pip, a simple command line utility `nmeadump` is automatically installed into the Python 3 scripts (bin) directory. This utility streams the parsed NMEA output of a GNSS/GPS device to the terminal.

Assuming the Python 3 scripts (bin) directory is in your PATH, the utility may be invoked thus (all args are optional):

`nmeadump port=/dev/ttyACM1 baud=9600 timeout=5 nmea_only=0 validate=1 raw=0`

If `nmea_only` is set to True (1), streaming will terminate on any non-NMEA data (e.g. UBX).

For help, type:

`nmeadump -h`

## Graphical Client

A python/tkinter graphical GPS client which supports both NMEA and UBX protocols is available at: 

[https://github.com/semuconsulting/PyGPSClient](https://github.com/semuconsulting/PyGPSClient)

---

## Author Information

![License](https://img.shields.io/github/license/semuconsulting/pynmeagps.svg)

semuadmin@semuconsulting.com
