import socket
import threading
from Messages.Imports import *
import EncoderDecoder
from Future import *

broadcast_addr = ('255.255.255.255', 3117)
# server_port = 80
# IP_broadcast = #"255.255.255.255"
BUFFER_SIZE = 586


class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.settimeout(5.0)
        self.receiving_buffer = []
        self.sending_buffer = []
        self.available_servers = []
        self.futures = []               # this list contains a list of future objects.
        self.listen = True
        self.hash_result = ""

    def stop_discovering(self):
        self.listen = False
        print "Stopped discovering"

    def start_discovering(self):
        self.listen = True
        print "Started discovering"

    def add_server(self, server):
        self.available_servers.append(server)

    def remove_server(self, server):
        self.available_servers.remove(server)

    def add_future(self, future_obj):
        self.futures.append(future_obj)

    def should_stop(self):
        for future_obj in self.futures:
            if future_obj.answer.type != 5:         # NAck
                return False
        return True

    def discover(self):
        print "Discovering servers"
        discover_message = Discover()
        discover_message.Init()
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client_socket.sendto(EncoderDecoder.encodeMessage(discover_message), broadcast_addr)
        time_out = threading.Timer(5.0, self.stop_discovering)
        time_out.start()

        while self.listen:
            print "waiting for an offer"
            try:
                data, address = self.client_socket.recvfrom(BUFFER_SIZE)
                msg = EncoderDecoder.decodeMessage(data)
                if msg.type == 2:
                    self.add_server(address)
                    print "Received an offer!"
            except:
                print "done"

    def num_to_word(self, num, len):
        letters = "abcdefghijklmnopqrstuvwxyz"
        remainder = num % 26
        rest = num / 26
        last_letter = letters[remainder]
        if len > 1:
            return self.num_to_word(rest, len-1) + last_letter
        else:
            return last_letter

    def divide_range(self, msg_length):
        # return array of pairs
        pairs = []
        num_of_servers = len(self.available_servers)
        end = 26 ** msg_length
        rng = (end / num_of_servers)
        for i in range(0, num_of_servers):
            pairs.append((self.num_to_word(int(i * rng), msg_length), self.num_to_word(int((i + 1) * rng) - 1, msg_length)))
        return pairs

    def send_to_servers(self, hash, msg_length):
        hash_range = self.divide_range(msg_length)

        for i, server in enumerate(self.available_servers):
            print "Request sent to " + str(server[0]) + " " + str(server[1])
            curr_hash_range = [hash_range[i][0], hash_range[i][1]]
            self.send_request(hash, msg_length, curr_hash_range[0], curr_hash_range[1], server)
            current_msg_result = Future()
            current_msg_result.Init(curr_hash_range, server)
            self.add_future(current_msg_result)
            current_msg_result.start_timer()
          #  self.remove_server(server)

    def send_request(self, hash, msg_length, start_s, end_s, server_add):
        # creating new request message
        request_msg = Request()
        request_msg.Init(hash, msg_length, start_s, end_s)
        self.client_socket.sendto(EncoderDecoder.encodeMessage(request_msg), server_add)

    def timeout_treatment(self, hash, msg_length):
        timeout_futures = []
        for future_obj in self.futures:
            if future_obj.is_timeout():
                timeout_futures.append(future_obj)

        self.discover()

        for i, server in enumerate(self.available_servers):
            if i >= len(timeout_futures):
                break

            curr_future = timeout_futures[i]    # getting the current future

            self.send_request(hash, msg_length, curr_future.string_range[0],
                              curr_future.string_range[1], server)
            # changing the server address in future object
            curr_future.server = server
            curr_future.start_timer()
            # remove server
            self.remove_server(server)

    def set_future_nack(self, curr_ip, curr_port, result):
        for future_obj in self.futures:
            future_ip, future_port = future_obj.server
            if future_ip == curr_ip and future_port == curr_port:
                future_obj.update_answer(result)

    def receive_msg(self):
        print "Trying to receive"
        if self.should_stop():
            return True
        print "Should Receive"
        data, address = self.client_socket.recvfrom(BUFFER_SIZE)
        msg = EncoderDecoder.decodeMessage(data)
        print "Received!!! type - " + str(msg.type)
        if msg.type == 4:  # ACK
            curr_hash_result = msg.origin_start
            if EncoderDecoder.valid_ack(curr_hash_result):  # HURRAY
                self.hash_result = curr_hash_result
                return True
        elif msg.type == 5:  # NAck
            self.set_future_nack(address[0], address[1], msg)
        return False

    def communicate(self, hash, msg_length):
        self.discover()
        self.send_to_servers(hash, msg_length)
        while self.receive_msg():
            self.timeout_treatment(hash, msg_length)
        return self.hash_result
