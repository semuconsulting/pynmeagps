"""
quecteldemo.py

A simple demonstrator for Quectel LG290P configuration and monitoring support in pynmeagps.

Usage:

python3 quecteldemo.py port=/dev/ttyACM0 baudrate=38400 timeout=3 qtmonly=1

The 'qtmonly' boolean argument can be used to limit displayed output to
proprietary PQTM messages only.

It implements two threads which run concurrently:
1) an I/O thread which continuously reads NMEA data from the
receiver and sends any queued outbound command or poll messages.
2) a process thread which processes parsed NMEA data - in this example
it simply prints the parsed data to the terminal.
NMEA data is passed between threads using queues.

NB: Some LG290P commands require a hot reset (PQTMHOT)
or a parameter save (PQTMSAVEPAR) and a full system reset (PQTMSRR)
before taking effect.

Press CTRL-C to terminate.

Created on 19 Aug 2024

:author: semuadmin
:copyright: SEMU Consulting Â© 2021
:license: BSD 3-Clause
"""

from queue import Queue
from sys import argv
from threading import Event, Thread
from time import sleep

from serial import Serial

from pynmeagps import POLL, SET, NMEAMessage, NMEAReader, hex2str

# standard NMEA messages which can be set using PQTMCFGMSGRATE
# NB don't need msgver with these message types
LG290P_STANDARD_MESSAGES = [
    "GGA",
    "GLL",
    "GSA",
    "GSV",
    "RMC",
    "VTG",
]
# proprietary NMEA messages which can be set using PQTMCFGMSGRATE
# NB need msgver with these message types
LG290P_PROPRIETARY_MESSAGES = [
    ("PQTMDOP", 1),  # Outputs Dilution of Precision
    ("PQTMEPE", 2),  # Output Estimated Position Error
    ("PQTMGEOFENCESTATUS", 1),  # Outputs Geofence Status
    ("PQTMODO", 1),  # Outputs Odometer Information
    ("PQTMPL", 1),  # Outputs Protection Level Information
    ("PQTMPVT", 1),  # Outputs PVT (GNSS) Result
    ("PQTMSVINSTATUS", 1),  # Outputs Survey-In Status
    ("PQTMTXT", 1),  # Outputs Short Text Message
    ("PQTMVEL", 1),  # Output Velocity Information
]


def io_data(
    nmr: NMEAReader,
    readqueue: Queue,
    sendqueue: Queue,
    stop: Event,
):
    """
    THREADED
    Read and parse inbound NMEA data and place
    raw and parsed data on queue.

    Send any queued outbound messages to receiver.
    """
    # pylint: disable=broad-exception-caught

    while not stop.is_set():
        try:
            (raw_data, parsed_data) = nmr.read()
            if parsed_data:
                readqueue.put((raw_data, parsed_data))

            while not sendqueue.empty():
                data = sendqueue.get()
                if data is not None:
                    nmr.datastream.write(data.serialize())
                sendqueue.task_done()

        except Exception as err:
            print(f"\n\nSomething went wrong {err}\n\n")
            continue


def process_data(queue: Queue, stop: Event, qtmonly: bool):
    """
    THREADED
    Get NMEA data from queue and display.
    """

    while not stop.is_set():
        if queue.empty() is False:
            (_, parsed) = queue.get()
            if not (qtmonly and "QTM" not in parsed.identity):
                print(f"Receiving {parsed}")
            queue.task_done()


def send(queue: Queue, msg: NMEAMessage, delay: float = 0.1):
    """
    Place message on send queue.
    """

    print(f"Sending {msg} ...")
    queue.put(msg)
    sleep(delay)


def main(**kwargs):
    """
    Main routine.
    """

    port = kwargs.get("port", "/dev/ttyAMA0")
    baudrate = int(kwargs.get("baudrate", 460800))
    timeout = float(kwargs.get("timeout", 3))
    qtmonly = int(kwargs.get("qtmonly", 0))

    with Serial(port, baudrate, timeout=timeout) as serial_stream:
        nmeareader = NMEAReader(serial_stream)

        read_queue = Queue()
        send_queue = Queue()
        stop_event = Event()

        io_thread = Thread(
            target=io_data,
            args=(
                nmeareader,
                read_queue,
                send_queue,
                stop_event,
            ),
        )
        process_thread = Thread(
            target=process_data,
            args=(
                read_queue,
                stop_event,
                qtmonly,
            ),
        )

        print("\nStarting handler threads. Press Ctrl-C to terminate...")
        io_thread.start()
        process_thread.start()

        try:
            # *******************************************************************
            # COMMENT/UNCOMMMENT LG290P COMMANDS (SET) OR QUERIES (POLL) HERE...
            #
            # Refer to testConstructors_QUECTEL() in tests\test_quectel.py
            # for a complete set of example LG290P message constructors
            # *******************************************************************

            # query version number
            msg = NMEAMessage("P", "QTMVERNO", POLL)
            send(send_queue, msg)

            # do factory reset (NB only takes effect after restart)
            msg = NMEAMessage("P", "QTMRESTOREPAR", SET)
            send(send_queue, msg)

            # save settings to non-volatile memory
            # msg = NMEAMessage("P", "QTMSAVEPAR", SET)
            # send(send_queue, msg)

            # turn debug mode on
            # msg = NMEAMessage("P", "QTMDEBUGON", SET)
            # send(send_queue, msg)

            # turn debug mode off
            # msg = NMEAMessage("P", "QTMDEBUGOFF", SET)
            # send(send_queue, msg)

            # check receiver mode (1 = Rover)
            msg = NMEAMessage("P", "QTMCFGRCVRMODE", POLL)
            send(send_queue, msg)

            # set fix rate to 1Hz (NB requires hot restart PQTMHOT to take effect)
            msg = NMEAMessage("P", "QTMCFGFIXRATE", SET, fixinterval=1000)
            send(send_queue, msg)

            # check to see if fix rate has been updated
            msg = NMEAMessage("P", "QTMCFGFIXRATE", POLL)
            send(send_queue, msg)

            # *************************************************
            # NB! PQTMCFGUART command has several permutations:
            # *************************************************

            # set baud rate on current UART, leaving other parameters unchanged
            NMEAMessage("P", "QTMCFGUART", SET, baudrate=460800)
            send(send_queue, msg)

            # set baud rate on UART2 interface (portid=2), leaving other parameters unchanged
            NMEAMessage("P", "QTMCFGUART", SET, portid=2, baudrate=115200)
            send(send_queue, msg)

            # configure all parameters on current UART
            NMEAMessage(
                "P",
                "QTMCFGUART",
                SET,
                baudrate=460800,
                databit=8,
                parity=0,
                stopbit=1,
                flowctrl=0,
            )
            send(send_queue, msg)

            # configure all parameters on UART2 interface (portid=2)
            NMEAMessage(
                "P",
                "QTMCFGUART",
                SET,
                portid=2,
                baudrate=115200,
                databit=8,
                parity=0,
                stopbit=1,
                flowctrl=0,
            )
            send(send_queue, msg)

            # check UART config for all 3 available ports
            for portid in range(1, 4):
                msg = NMEAMessage("P", "QTMCFGUART", POLL, portid=portid)
                send(send_queue, msg)
                msg = NMEAMessage("P", "QTMCFGPROT", POLL, porttype=1, portid=portid)
                send(send_queue, msg)

            # turn gnss engine off
            # msg = NMEAMessage("P", "QTMGNSSSTOP", SET)
            # send(send_queue, msg)

            # turn gnss engine on
            # msg = NMEAMessage("P", "QTMGNSSSTART", SET)
            # send(send_queue, msg)

            # do cold start
            # msg = NMEAMessage("P", "QTMCOLD", SET)
            # send(send_queue, msg)

            # do warm start
            # msg = NMEAMessage("P", "QTMWARM", SET)
            # send(send_queue, msg)

            # set satellite mask (see also PQTMCFGCNST)
            NMEAMessage(
                "P",
                "QTMCFGSAT",
                SET,
                systemid=1,
                signalid=1,
                masklow=hex2str(0xFFFFFFFF, 8),  # hex as padded string
            )
            send(send_queue, msg)

            # set signal masks
            NMEAMessage(
                "P",
                "QTMCFGSIGNAL",
                SET,
                gpssig=hex2str(0x07),  # hex as unpadded string
                glonasssig=hex2str(0x03),
                galileosig=hex2str(0x0F),
                beidousig=hex2str(0x3F),
                qzsssig=hex2str(0x07),
                navicsig=hex2str(0x01),
            )
            send(send_queue, msg)

            # disable all standard NMEA messages
            for msgname in LG290P_STANDARD_MESSAGES:
                msg = NMEAMessage("P", "QTMCFGMSGRATE", SET, msgname=msgname, rate=0)
                send(send_queue, msg)

            # enable all proprietary NMEA messages
            for msgname, msgver in LG290P_PROPRIETARY_MESSAGES:
                msg = NMEAMessage(
                    "P", "QTMCFGMSGRATE", SET, msgname=msgname, rate=1, msgver=msgver
                )
                send(send_queue, msg)

            # *********************************************************************
            # NB! Base and Rover configurations require 3 or 4 commends in sequence
            # *********************************************************************

            # Set Base Station, Survey-In Mode - requires 4 commands in sequence:
            msg1 = NMEAMessage("P", "QTMCFGRCVRMODE", SET, rcvrmode=2)
            msg2 = NMEAMessage(
                "P", "QTMCFGSVIN", SET, svinmode=1, cfgcnt=60, acclimit=3000
            )
            msg3 = NMEAMessage(
                "P",
                "QTMSAVEPAR",
                SET,
            )
            msg4 = NMEAMessage(
                "P",
                "QTMSRR",
                SET,
            )
            msgs = [msg1, msg2, msg3, msg4]
            for msg in msgs:
                send(send_queue, msg)

            # Set Base Station, Fixed Mode - requires 4 commands in sequence:
            # msg1 = NMEAMessage("P", "QTMCFGRCVRMODE", SET, rcvrmode=2)
            # msg2 = NMEAMessage(
            #     "P",
            #     "QTMCFGSVIN",
            #     SET,
            #     svinmode=2,
            #     cfgcnt=0,
            #     acclimit=0,
            #     exefx=-2213540.321087019,
            #     ecefy=-4577229.071167925,
            #     ecefz=3838042.2419518335,
            # )
            # msg3 = NMEAMessage(
            #     "P",
            #     "QTMSAVEPAR",
            #     SET,
            # )
            # msg4 = NMEAMessage(
            #     "P",
            #     "QTMSRR",
            #     SET,
            # )
            # msgs = [msg1, msg2, msg3, msg4]
            # for msg in msgs:
            #     send(send_queue, msg)

            # Reset to Normal (Rover) Mode - requires 3 commands in sequence:
            msg1 = NMEAMessage("P", "QTMCFGRCVRMODE", SET, rcvrmode=1)
            msg2 = NMEAMessage(
                "P",
                "QTMSAVEPAR",
                SET,
            )
            msg3 = NMEAMessage(
                "P",
                "QTMSRR",
                SET,
            )
            msgs = [msg1, msg2, msg3]
            for msg in msgs:
                send(send_queue, msg)

            # check geofence config
            # for index in range(0, 4):
            #     msg = NMEAMessage("P", "QTMCFGGEOFENCE", POLL, index=index)
            #     send(send_queue, msg)

            # # check satellite config (signal 1 only in this example)
            # for systemid in range(1, 7):
            #     msg = NMEAMessage("P", "QTMCFGSAT", POLL, systemid=systemid, signalid=1)
            #     send(send_queue, msg)

            # do hot start (required after setting fix rate or satellite config)
            msg = NMEAMessage("P", "QTMHOT", SET)
            send(send_queue, msg, 1)

            while not stop_event.is_set():  # loop until user presses Ctrl-C
                sleep(1)

        except KeyboardInterrupt:  # capture Ctrl-C
            print("\n\nTerminated by user.")
            stop_event.set()

        print("\nStop signal set. Waiting for threads to complete...")
        io_thread.join()
        process_thread.join()
        print("\nProcessing complete")


if __name__ == "__main__":

    main(**dict(arg.split("=") for arg in argv[1:]))
