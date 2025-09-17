"""
nmeapoller.py

This example illustrates how to read, write and display NMEA messages
"concurrently" using threads and queues. This represents a useful
generic pattern for many end user applications.

Usage:

python3 nmeapoller.py port=/dev/ttyACM0 baudrate=38400 timeout=3

It implements two threads which run concurrently:
1) an I/O thread which continuously reads NMEA data from the
receiver and sends any queued outbound command or poll messages.
2) a process thread which processes parsed NMEA data - in this example
it simply prints the parsed data to the terminal.
NMEA data is passed between threads using queues.

Press CTRL-C to terminate.

FYI: Since Python implements a Global Interpreter Lock (GIL),
threads are not strictly concurrent, though this is of minor
practical consequence here.

Created on 07 Aug 2021

:author: semuadmin (Steve Smith)
:copyright: semuadmin © 2021
:license: BSD 3-Clause
"""

from queue import Queue
from sys import argv
from threading import Event, Thread
from time import sleep

from serial import Serial

from pynmeagps import NMEA_MSGIDS, POLL, NMEAMessage, NMEAReader


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
                data = sendqueue.get(False)
                if data is not None:
                    nmr.datastream.write(data.serialize())
                sendqueue.task_done()

        except Exception as err:
            print(f"\n\nSomething went wrong {err}\n\n")
            continue


def process_data(queue: Queue, stop: Event):
    """
    THREADED
    Get NMEA data from queue and display.
    """

    while not stop.is_set():
        if queue.empty() is False:
            (_, parsed) = queue.get()
            print(parsed)
            queue.task_done()


def main(**kwargs):
    """
    Main routine.
    """

    port = kwargs.get("port", "/dev/ttyACM0")
    baudrate = int(kwargs.get("baudrate", 38400))
    timeout = float(kwargs.get("timeout", 3))

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
            ),
        )

        print("\nStarting handler threads. Press Ctrl-C to terminate...")
        io_thread.start()
        process_thread.start()

        # loop until user presses Ctrl-C
        while not stop_event.is_set():
            try:
                # DO STUFF IN THE BACKGROUND...
                # Poll for each NMEA sentence type.
                # NB: Your receiver may not support all types. It will return a
                # GNTXT "NMEA unknown msg" response for any types it doesn't support.
                for msgid in NMEA_MSGIDS:
                    print(
                        f"\nSending a GNQ message to poll for an {msgid} response...\n"
                    )
                    msg = NMEAMessage("EI", "GNQ", POLL, msgId=msgid)
                    send_queue.put(msg)
                    sleep(1)
                sleep(3)
                stop_event.set()

            except KeyboardInterrupt:  # capture Ctrl-C
                print("\n\nTerminated by user.")
                stop_event.set()

        print("\nStop signal set. Waiting for threads to complete...")
        io_thread.join()
        process_thread.join()
        print("\nProcessing complete")


if __name__ == "__main__":

    main(**dict(arg.split("=") for arg in argv[1:]))
