import struct
from Messages.Imports import *

packing_format = 'B40sB256s256s'

def encodeMessage(msg):
    hashUtf8 = msg.hash.encode('utf-8')
    originStartUtf8 = msg.origin_start.encode('utf-8')
    originEndUtf8 = msg.origin_end.encode('utf-8')
    encodedM = struct.pack(packing_format, msg.type, hashUtf8, msg.origin_length, originStartUtf8, originEndUtf8)
    return encodedM

def decodeMessage(buffer):
    encodedM = struct.unpack(packing_format, buffer)
    type = encodedM[0]
    hash = encodedM[1].decode('utf-8')
    origin_length = encodedM[2]
    origin_start = encodedM[3].decode('utf-8')
    origin_end = encodedM[4].decode('utf-8')

    msg = None

    if type == 1:
        msg = Discover()
        msg.Init()

    elif type == 2:
        msg = Offer()
        msg.Init()

    elif type == 3:
        msg = Request()
        msg.Init(hash, origin_length, origin_start, origin_end)

    elif type == 4:
        msg = Ack()
        msg.Init()

    elif type == 5:
        msg = NAck()
        msg.Init(hash, origin_length)

    else:
        raise Exception("Invalid type")

    return msg
