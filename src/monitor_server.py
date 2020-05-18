import microbit
import time
import os
import json
import sys
from urllib import urlopen
import time
import numpy as np
import config

from websocket import create_connection


from config import *

from future.standard_library import install_aliases
install_aliases()


HOST = '0.0.0.0'
PORT = 8080


x = np.arange(1,257)
calib = np.log(x)

if len(sys.argv) > 0:
    HOST = str(sys.argv[1])
    try:
        ROT = float(sys.argv[2])
    except IndexError:
        ROT = 90.
    try:
        DISP = str(sys.argv[3])
    except IndexError:
        DISP = "raw"

URL = "ws://{}:{}/ws".format(HOST, PORT)
TEST_URL = "http://{}:{}".format(HOST, PORT)

def wait_for_internet_connection():
    while True:
        try:
            print("trying {}".format(TEST_URL))
            response = urlopen(TEST_URL,timeout=1)
            break
        except IOError:
            awaiting_connection()
        except ConnectionRefusedError:
            awaiting_connection()
    return


def process_sound(sound):
    levels = np.abs((sound['data']*calib)) #sound['data']
    rgb = []
    if np.mean(levels) > 0.07:
        cry = True
        msg = 'C'
    else:
        cry = False
        msg = 'Q'
    microbit.send_message(msg)
    return

def awaiting_connection():
    # rgb = wifi_rgb[randint(0,5)]
    microbit.send_message('W')
    time.sleep(0.1)
    return

def run(ws):
    while True:
        ws.send(".")
        message =  ws.recv()
        sound = json.loads(message)
        process_sound(sound)
    return

if __name__ == "__main__":
    while True:
        wait_for_internet_connection()

        try:
            ws = create_connection(URL)
            run(ws)
        except KeyboardInterrupt:
            unicornhathd.off()
            ws.close()
            break
        except ConnectionResetError:
            pass
