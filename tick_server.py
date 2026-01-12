#
# Simple Tick Data Server
#
import zmq
import json
import time
import random
import datetime

context = zmq.Context()
socket = context.socket(zmq.PUB)  # PUBLISHER = SERVER
socket.bind('tcp://127.0.0.1:5555')

AAPL = 100.
MSFT = 100.

while True:
    if random.random() > 0.5:
        SYM = 'AAPL'
        AAPL += random.gauss(0, 1) / 2
        PRICE = round(AAPL, 2)
    else:
        SYM = 'MSFT'
        MSFT += random.gauss(0, 1) / 3
        PRICE = round(MSFT, 2)
    TIME = str(datetime.datetime.now())
    data = {'TIME': TIME, 'SYMBOL': SYM, 'PRICE': PRICE}
    print(data)
    socket.send_string(json.dumps(data))
    time.sleep(random.random() * 2)
