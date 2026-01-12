#
# Simple Tick Data Client
#
import zmq
import json
import datetime

context = zmq.Context()
socket = context.socket(zmq.SUB)  # SUBSCRIBER = CLIENT (LISTENER)
socket.connect('tcp://127.0.0.1:5555')
socket.setsockopt_string(zmq.SUBSCRIBE, '')

while True:
    msg = socket.recv_string()
    t = str(datetime.datetime.now())
    data = json.loads(msg)
    print(t)
    print(data)
