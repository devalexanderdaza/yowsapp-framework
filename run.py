import sys, logging, config

from yowsup.layers.axolotl.props import PROP_IDENTITY_AUTOTRUST
from yowsup.stacks import YowStackBuilder
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from consonance.structs.keypair import KeyPair
import base64

from app.layer import MacLayer

import threading
from flask import Flask, request, g
from app.utils import helper
import json

# Uncomment to log
#logging.basicConfig(level=logging.DEBUG)

# Config
credentials = config.credentials['phone'], KeyPair.from_bytes(base64.b64decode(config.credentials['password']))
encryption = True

class WS(object):
    def __init__(self):
        self.app = Flask(__name__)

        @self.app.route("/send", methods=['POST'])
        def send():            
            body = request.json
            MacLayer.send_message(body['text'].replace("\n", "\n"), body['conversation'])
            return helper.json_response(status=201)

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            
        thread.start() 

    def run(self):
        while True:
            self.app.run()


class MacStack(object):
    def __init__(self):
        builder = YowStackBuilder()

        self.stack = builder \
            .pushDefaultLayers() \
            .push(MacLayer) \
            .build()
        self.stack.setCredentials(credentials)
        self.stack.setProp(MacLayer.PROP_CONTACTS, list(config.contacts.keys()))
        self.stack.setProp(PROP_IDENTITY_AUTOTRUST, True)

    def start(self):
        print("[Whatsapp] Mac started\n")
        print("[Whatsapp] Current State:", YowNetworkLayer.EVENT_STATE_CONNECT)
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))

        try:
            self.stack.loop(timeout=0.5, discrete=0.5)
        except KeyboardInterrupt:
            print("\nYowsdown")
            sys.exit(0)


def run_infinite():
    while True:
        try:
            c = MacStack()
            c.start()
        except:
            pass
        else:
            break


if __name__ == "__main__":
    WS()
    c = MacStack()
    c.start()