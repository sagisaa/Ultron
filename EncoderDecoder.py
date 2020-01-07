import struct
from Messages.Imports import *

packing_format = '32sB40sB256s256s'

def encodeMessage(msg):
    teamUtf8 = msg.team_name.encode('utf-8')
    hashUtf8 = msg.hash.encode('utf-8')
    originStartUtf8 = msg.origin_start.encode('utf-8')
    originEndUtf8 = msg.origin_end.encode('utf-8')
    encodedM = struct.pack(packing_format, teamUtf8, msg.type, hashUtf8, msg.origin_length, originStartUtf8, originEndUtf8)
    return encodedM


def decodeMessage(buffer):
    encodedM = struct.unpack(packing_format, buffer)
    team = encodedM[0].rstrip('\x00')
    type = encodedM[1]
    hash = encodedM[2].rstrip('\x00')
    origin_length = encodedM[3]
    origin_start = encodedM[4].rstrip('\x00')
    origin_end = encodedM[5].rstrip('\x00')

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
        msg.Init(hash, origin_length, origin_start)

    elif type == 5:
        msg = NAck()
        msg.Init(hash, origin_length)

    else:
        print(buffer)
        raise Exception("Invalid type: " + str(encodedM[0]) + str(encodedM[1]))

    return msg

