#
# This is a simple HTTP Server utilising the native
# Python 3 http.server library.
#
# It implements a REST API /gps to retrieve GPS data
# from the designated GPSClass object.
#

from http.server import SimpleHTTPRequestHandler, HTTPServer
import json
import random
from datetime import datetime

ADDRESS = "localhost"
TCPPORT = 8080
HTML = "/index.html"
CSS = "/styles.css"
JS = "/scripts.js"


class GPSDataStub:
    """
    Stub data class to simulate GPS data.
    """

    def get_data(self):
        """
        Return simulated GPS data in JSON format.
        """

        now = datetime.now()
        dic = {
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
            "latitude": round(random.uniform(-90.0, 90.0), 5),
            "longitude": round(random.uniform(-180.0, 180.0), 5),
            "elevation": round(random.uniform(-50.0, 100.0), 2),
            "speed": round(random.uniform(0, 100.0), 2),
            "track": round(random.uniform(0, 360.0), 2),
            "siv": random.randrange(0, 33),
            "pdop": round(random.uniform(0, 99.0), 2),
            "hdop": round(random.uniform(0, 99.0), 2),
            "vdop": round(random.uniform(0, 99.0), 2),
            "fix": random.randrange(1, 4),
        }
        return json.dumps(dic)


class GPSHTTPServer(HTTPServer):
    """
    HTTPServer subclass incorporating reference to GPS streamer class
    in support of the /gps REST API.

    gpsClass must implement a get_data() method which returns a JSON
    payload.
    """

    def __init__(self, server_address, RequestHandlerClass, GPSClass):
        """
        Constructor.
        """

        self.gps = GPSClass
        super().__init__(server_address, RequestHandlerClass)


class GPSHTTPHandler(SimpleHTTPRequestHandler):
    """
    HTTP Request Handler subclass.
    """

    def do_GET(self):
        """
        Handle GET request.
        """

        if self.path == "/":
            self.path = HTML

        mimetype = self.guess_type(self.path)
        rc = 200

        if self.path in (HTML, JS, CSS):
            res = open(self.path[1:]).read()
        elif self.path == "/gps":  # invoke GPS REST API
            res = self.server.gps.get_data()
            mimetype = "application/json"
        else:
            res = "Unknown Request"
            rc = 501

        self.send_response(rc)
        self.send_header("Content-type", mimetype)
        self.end_headers()
        self.wfile.write(res.encode())


if __name__ == "__main__":

    GPSClass = GPSDataStub()
    print("\nStarting HTTP Server on http://" + ADDRESS + ":" + str(TCPPORT) + " ...")
    httpd = GPSHTTPServer((ADDRESS, TCPPORT), GPSHTTPHandler, GPSClass)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.shutdown()

    print("\nHTTP Server stopped.")
