import struct
from Message import *
import random

packing_format = '32sB40sB256s256s'
header_format = '32sB40sB'
unpacking_header_msg = '32sB40sBss'
TYPE_LOC = 32
HASH_LOC = 33
ORIGIN_LENGTH_LOC = 73
ORIGIN_START_LOC = 74
def encodeMessage(msg):

    team = msg.team_name
    type = msg.type
    curr_hash = msg.hash
    origin_length = msg.origin_length
    origin_start = msg.origin_start
    origin_end = msg.origin_end

    team_bytes = team.ljust(32).encode('utf-8')
    type_byte = bytes([type])
    hash_bytes = curr_hash.encode('utf-8')
    origin_length_byte = bytes([origin_length])
    origin_start_bytes = origin_start.encode('utf-8')
    origin_end_bytes = origin_end.encode('utf-8')
    return team_bytes + type_byte + hash_bytes + origin_length_byte + origin_start_bytes + origin_end_bytes


def decodeMessage(buffer):
    try:
        team_name = buffer[0:32].decode('utf-8').strip()
        type = int(buffer[TYPE_LOC])
        curr_hash = buffer[HASH_LOC:(HASH_LOC + 40)].decode('utf-8')
        origin_length = int(buffer[ORIGIN_LENGTH_LOC])
        remaining_str = buffer[ORIGIN_START_LOC:]
        origin_start = remaining_str[0:origin_length].decode('utf-8')
        origin_end = remaining_str[origin_length:].decode('utf-8')

        # Check valid!!
        msg = Message(team_name, type, curr_hash, origin_length, origin_start, origin_end)

        return msg

    except:
        return None

def get_start_end(length):
    chrs = 'abcdef'
    return ''.join(random.choice(chrs) for _ in range(length))
