import hashlib
import threading
import socket
from Message import *
import EncoderDecoder
from Ranger import Ranger
import Server
import time

TIME_OUT = 15

def num_to_word(num, len):
    letters = "abcdefghijklmnopqrstuvwxyz"
    remainder = num % 26
    rest = num / 26
    last_letter = letters[remainder]
    if len > 1:
        return num_to_word(rest, len - 1) + last_letter
    else:
        return last_letter

def word_to_num(word, len):
    letters = "abcdefghijklmnopqrstuvwxyz"
    num = 0
    for i in range(len-1, -1, -1):
        cur_dig = letters.index(word[i])
        num += cur_dig * (26 ** (len - i - 1))
    return num

def divide_range(msg_length, available_servers):
    # return array of pairs
    pairs = []
    num_of_servers = len(available_servers)
    end = 26 ** msg_length
    rng = (end / num_of_servers)
    for i in range(0, num_of_servers):
        pairs.append((num_to_word(int(i * rng), msg_length), num_to_word(int((i + 1) * rng) - 1, msg_length)))
    return pairs

def valid_ack(hash_result, maybe_word_input):
    if not hashlib.sha1(maybe_word_input.encode()).hexdigest() == hash_result:
        print(SELF_TEAM_NAME + " has detected a false alarm, sir.")
        print(maybe_word_input + " is not the answer.")
        print("Always at your service, sir.")
        return False
    return True

def calc_hash(request_msg, server_socket, client_address, lock_obj):
    hash_result = request_msg.hash
    hash_start = request_msg.origin_start
    hash_end = request_msg.origin_end
    hash_length = request_msg.origin_length
    answer = None
    client_ans = None
    num_start = word_to_num(hash_start, hash_length)
    num_end = word_to_num(hash_end, hash_length)
    i = num_start
    init_millis = int(round(time.time() * 1000))
    while i < num_end + 1 and int(round(time.time() * 1000)) - init_millis < TIME_OUT:
        word = num_to_word(i, hash_length)
        result = hashlib.sha1(word.encode()).hexdigest()
        if result == hash_result:
            print(SELF_TEAM_NAME + " has found an answer for team " + request_msg.team_name + ": " + str(word))
            answer = word
            break

    if answer is None:
        print(SELF_TEAM_NAME + " is too busy right now, and team " + request_msg.team_name + " is not helping!")
        client_ans = Message(SELF_TEAM_NAME, NACK_CODE, hash_result, hash_length, hash_start, hash_end)
    else:
        client_ans = Message(SELF_TEAM_NAME, ACK_CODE, hash_result, hash_length, answer, hash_end)

    lock_obj.acquire()
    Server.annoying_clients.remove((request_msg.team_name, client_address))
    server_socket.sendto(EncoderDecoder.encodeMessage(client_ans), client_address)
    lock_obj.release()
