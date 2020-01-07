import struct
from Message import *

packing_format = '32sB40sB256s256s'


def encodeMessage(msg):
    teamUtf8 = msg.team_name.encode('utf-8')
    hashUtf8 = msg.hash.encode('utf-8')
    originStartUtf8 = msg.origin_start.encode('utf-8')
    originEndUtf8 = msg.origin_end.encode('utf-8')
    encodedM = struct.pack(packing_format, teamUtf8, msg.type, hashUtf8, msg.origin_length, originStartUtf8,
                           originEndUtf8)
    return encodedM


def decodeMessage(buffer):
    try:
        encodedM = struct.unpack(packing_format, buffer)
        team = encodedM[0].rstrip('\x00')
        type = encodedM[1]
        hash = encodedM[2].rstrip('\x00')
        origin_length = encodedM[3]
        origin_start = encodedM[4].rstrip('\x00')
        origin_end = encodedM[5].rstrip('\x00')

        # Check valid!!
        msg = Message(team, type, hash, origin_length, origin_start, origin_end)

        return msg

    except:
        return None
