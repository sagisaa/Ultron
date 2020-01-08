import struct
from Message import *

header_format = '32sB40sB'
packing_format = '32sB40sB256s256s'
general_format = '32sB40sBs'

def encodeMessage(msg):
    teamUtf8 = msg.team_name.encode('utf-8')
    hashUtf8 = msg.hash.encode('utf-8')
    if msg.origin_length != 0:
        originStartUtf8 = msg.origin_start.encode('utf-8')
        originEndUtf8 = msg.origin_end.encode('utf-8')
        curr_msg_pack_format = header_format + str(msg.origin_length) + 's' + str(msg.origin_length) + 's'
        encodedM = struct.pack(curr_msg_pack_format, teamUtf8, msg.type, hashUtf8, msg.origin_length, originStartUtf8,
                               originEndUtf8)
    else:
        encodedM = struct.pack(header_format, teamUtf8, msg.type, hashUtf8, msg.origin_length)
    return encodedM


def decodeMessage(buffer):
    try:

        encodedM = struct.unpack(general_format, buffer)
        team = encodedM[0].rstrip('\x00')
        type = encodedM[1]
        hash = encodedM[2].rstrip('\x00')
        origin_length = encodedM[3]
        cur_format = str(origin_length) + 's' + str(origin_length) + 's'
        decoded_st_end = struct.unpack(cur_format, encodedM[4])
        origin_start = decoded_st_end[0]
        origin_end = decoded_st_end[1]

        # Check valid!!
        msg = Message(team, type, hash, origin_length, origin_start, origin_end)

        return msg

    except:
        return None
