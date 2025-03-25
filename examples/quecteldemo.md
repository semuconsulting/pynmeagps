PYNMEAGPS QUECTEL LG290P SUPPORT - NOTES
========================================

pynmeagps branch [quectel-lg290p-support](https://github.com/semuconsulting/pynmeagps/tree/quectel-lg290p-support) introduces _provisional_ support for the Quectel LG290P quad-band GNSS receiver. 

It aims to support the complete set of proprietary NMEA 0183 message types for LG290P output (GET), query (POLL) and command (SET), as documented in the
[Quectel_LG290P03_GNSS_Protocol_Specification_V1.0](https://quectel.com/content/uploads/2024/09/Quectel_LG290P03_GNSS_Protocol_Specification_V1.0.pdf).

**NB pynmeagps is an independent, free open-source project maintained entirely by unpaid volunteers. We have absolutely no affiliation with Quectel or its distributors.**

Assuming you have Python and pip on your platform, you can install this branch as follows:

```shell
python3 -m pip install git+https://github.com/semuconsulting/pynmeagps.git@quectel-lg290p-support
```

Refer to the [README](https://github.com/semuconsulting/pynmeagps) and [pynmeagps API documentation](https://www.semuconsulting.com/pynmeagps/) for implementation details, but here's a quick summary:

1. NMEA 0183 message identifiers comprise a "talker" and a "msgid". In the case of Quectel LG290P configuration, the talker will always be 'P' (Proprietary), the msgid will be "QTM...".

2. If you're creating or parsing NMEA messages, there are three message "modes" (`msgmode`) to consider:

    - GET (0x00) - output messages _from_ the receiver, including periodic navigation messages, query responses and command acknowledgements (ACK/NAK). This is the default mode.
    - SET (0x01) - configuration (state change) commands _to_ the receiver.
    - POLL (0x02) - queries _to_ the receiver in anticipation of a response back.

    If you're creating configuration commands for the LG290P, use `msgmode=0x01` (SET). If you're querying the current configuration, use `msgmode=0x02` (POLL). While parsing the output of the receiver, use `msgmode=0x00` (GET) - as this is the default, it doesn't need to be specified explicitly.

    (_**FYI** it's done this way because many protocols use the same message identifier for each "mode" but with different payload definitions, so pynmeagps needs to know which payload definition you want_)

    NB: the `status` attribute in the LG290P configuration messages is automatically set to "W" for commands (SET) and "R" for queries (POLL) - it does not need to be specified explicitly.

3. When creating NMEA messages using pynmeagps, you can _either_ specify the entire payload as a list - `payload=["W","PQTMPVT","1"]` - _or_ you can provide a series of key/value arguments corresponding to the individual attributes for that message type - `msgname="PQTMPVT", rate=1`. Any attributes that you omit will be set to their default type value (e.g. numeric will default to 0) **NB** this is the _type_ default, which is _not necessarily_ the LG290P's firmware default. This is particularly relevant when using the long form of the PQTMCFGUART command e.g. if you omit the `databit` and `stopbit` arguments, they will both default to 0, rather than the firmware defaults of 8 and 1 respectively.

4. Some configuration commands exist in multiple variants e.g. `PQTMCFGUART` and `PQTMCFGMSGRATE`. The variant created by pynmeagps depends on the key/value arguments provided e.g. for the `PQTMCFGUART` message, including the `portid` key/value will create the 'specified interface' form of the command; omitting the `portid` key/value will create the shorter 'current interface' form. Refer to the Quectel documentation for examples.

5. You need to serialize the messages before sending them to the receiver's UART interface - you can use the `NMEAMessage.serialize()` function for this.

6. For example:

    ```python
    from serial import Serial
    from pynmeagps import NMEAMessage, SET

    # set message rate for PQMTPVT output message
    msg = NMEAMessage("P", "QTMCFGMSGRATE", SET, msgname="PQTMPVT", rate=1, msgver=1)
    print(msg)
    print(msg.serialize())

    # set UART configuration, short form; sets baudrate on current interface, leaving other parameters unchanged   
    msg = NMEAMessage("P", "QTMCFGUART", SET, baudrate=115200) 
    print(msg)
    print(msg.serialize())
    # set UART configuration, long form; sets all parameters on specified (UART2) interface
    msg = NMEAMessage("P", "QTMCFGUART", SET, portid=2, baudrate=115200, databit=8, parity=0, stopbit=1, flowctrl=0)
    print(msg)
    print(msg.serialize())

    # send serialized message to receiver - amend port and baudrate as required
    stream = Serial("\dev\ttyACM1", 115200, timeout=3)
    stream.write(msg.serialize())
    ```

    The printed output should be:
    ```shell
    <NMEA(PQTMCFGMSGRATE, status=W, msgname=PQTMPVT, rate=1, msgver=1)>
    b'$PQTMCFGMSGRATE,W,PQTMPVT,1,1*1C\r\n'
    <NMEA(PQTMCFGUART, status=W, baudrate=115200)>
    b'$PQTMCFGUART,W,115200*18\r\n'
    <NMEA(PQTMCFGUART, status=W, portid=2, baudrate=115200, databit=8, parity=0, stopbit=1, flowctrl=0)>
    b'$PQTMCFGUART,W,2,115200,8,0,1,0*0F\r\n'
    ```

7. There is a basic demo script [quecteldemo.py](https://github.com/semuconsulting/pynmeagps/blob/quectel-lg290p-support/examples/quecteldemo.py) in the \examples folder which illustrates how to send commands or queries to the receiver while simultaneously parsing the output - this should allow you to monitor the effects of any configuration changes or queries in real time. **NB** certain config changes may require an explicit reconnection or even a power cycle (e.g. baud rate change or factory reset) - refer to the Quectel documentation for details.

8. The unit test cases used by pynmeagps's automated build process can be found in [test_quectel.py](https://github.com/semuconsulting/pynmeagps/blob/quectel-lg290p-support/tests/test_quectel.py)
