# tvdatafeed/tvsession.py

import random
import string
import websocket
import json
import time
import uuid
from threading import Thread
from .const import TRADINGVIEW_HEADERS

class TVSession:
    def __init__(self):
        self.session = self._generate_session()
        self.ws = None
        self.connected = False
        self.thread = None
        self.responses = []

    def _generate_session(self):
        return 'qs_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))

    def connect(self):
        self.ws = websocket.WebSocketApp(
            "wss://prodata.tradingview.com/socket.io/websocket",
            header=TRADINGVIEW_HEADERS,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close,
            on_open=self.on_open
        )
        self.thread = Thread(target=self.ws.run_forever)
        self.thread.daemon = True
        self.thread.start()

        while not self.connected:
            time.sleep(0.1)

    def on_message(self, ws, message):
        if message.startswith("~m~"):
            length = int(message[3:message.find("~m~", 3)])
            content = message[message.find("~m~", 3) + 3:][:length]
            data = json.loads(content)
            self.responses.append(data)

    def on_error(self, ws, error):
        print(f"TVSession Error: {error}")

    def on_close(self, ws):
        self.connected = False
        print("TVSession Closed")

    def on_open(self, ws):
        self.connected = True
        print("TVSession Opened")

    def send(self, data):
        payload = json.dumps(data)
        message = f"~m~{len(payload)}~m~{payload}"
        self.ws.send(message)

    def close(self):
        self.ws.close()
