import socket
import threading
import Hash
from Message import *
import EncoderDecoder
from Future import *

broadcast_addr = ('255.255.255.255', 3117)
BUFFER_SIZE = 586

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.client_socket.settimeout(15.0)
        self.available_servers = []
        self.futures = []               # this list contains a list of future objects.
        self.listen = True
        self.hash_result = ""
        self.found_result = False

    def stop_discovering(self):
        self.listen = False
        print(SELF_TEAM_NAME + " stopped scanning for offers..")

    def start_discovering(self):
        self.listen = True
        print(SELF_TEAM_NAME + " started scanning for offers..")

    def add_server(self, server, team_name):
        self.available_servers.append((server, team_name))

    def add_future(self, future_obj):
        self.futures.append(future_obj)

    def should_stop(self):
        if self.found_result:
            return True
        for future_obj in self.futures:
            if future_obj.answer.type != 5:         # NAck
                return False
        return True

    def discover(self, hash, msg_length):
        self.start_discovering()
        discover_message = Message(SELF_TEAM_NAME, DISCOVER_CODE, hash, msg_length,
                                   "".ljust(msg_length), "".ljust(msg_length))
        self.client_socket.sendto(EncoderDecoder.encodeMessage(discover_message), broadcast_addr)
        time_out = threading.Timer(5.0, self.stop_discovering)
        time_out.start()

        while self.listen:
            is_received = False
            try:
                data = []
                data, address = self.client_socket.recvfrom(BUFFER_SIZE)
                is_received = True
                msg = EncoderDecoder.decodeMessage(data)
                if msg is not None:
                    if msg.type == 2:
                        # if self.available_servers.count(address) == 0:
                        self.add_server(address, msg.team_name)
                        print("Received an offer from team " + msg.team_name + ", address: " + str(address))
                    else:
                        print("Very funny, team " + msg.team_name + ".. An offer was expected.")
                else:
                    print("Received garbage from address " + str(address))
            except:
                if is_received:
                    print("What the hell is this?")

    def send_to_servers(self, hash, msg_length):
        hash_range = Hash.divide_range(msg_length, self.available_servers)

        for i, (server, team_name) in enumerate(self.available_servers):
            print("Request sent to team " + team_name + ", address: " + str(server))
            curr_hash_range = [hash_range[i][0], hash_range[i][1]]
            self.send_request(hash, msg_length, curr_hash_range[0], curr_hash_range[1], server)
            current_msg_result = Future()
            current_msg_result.Init(curr_hash_range, server)
            self.add_future(current_msg_result)
            current_msg_result.start_timer()

        self.filter_servers()

    def send_request(self, hash, msg_length, start_s, end_s, server_add):
        # creating new request message
        request_msg = Message(SELF_TEAM_NAME, REQUEST_CODE, hash, msg_length, start_s, end_s)
        self.client_socket.sendto(EncoderDecoder.encodeMessage(request_msg), server_add)

    def filter_servers(self):
        filtered_servers = []
        for (server, team_name) in self.available_servers:
            used_server = False
            for future_obj in self.futures:
                if future_obj.server == server and not future_obj.is_timeout():
                    used_server = True
                    break
            if not used_server:
                filtered_servers.append((server, team_name))
        self.available_servers = filtered_servers

    def timeout_treatment(self, hash, msg_length):
        timeout_futures = []
        for future_obj in self.futures:
            if future_obj.is_timeout():
                timeout_futures.append(future_obj)

        self.discover(hash, msg_length)
        self.filter_servers()
        for i, (server, team_name) in enumerate(self.available_servers):
            if i >= len(timeout_futures):
                break

            curr_future = timeout_futures[i]    # getting the current future

            self.send_request(hash, msg_length, curr_future.string_range[0],
                              curr_future.string_range[1], server)
            # changing the server address in future object
            curr_future.server = server
            curr_future.start_timer()
            # remove server

        self.filter_servers()

    def set_future_nack(self, curr_ip, curr_port, result):
        for future_obj in self.futures:
            future_ip, future_port = future_obj.server
            if future_ip == curr_ip and future_port == curr_port:
                future_obj.update_answer(result)

    def receive_msg(self, hash):
        print("Trying to receive")
        if self.should_stop():
            return False
        print("Should Receive")
        try:
            data, address = self.client_socket.recvfrom(BUFFER_SIZE)
            msg = EncoderDecoder.decodeMessage(data)
            if msg is not None:
                print("Received!!! type - " + str(msg.type))
                if msg.type == 4:  # ACK
                    curr_hash_result = msg.origin_start
                    if Hash.valid_ack(hash, curr_hash_result):  # HURRAY
                        print("Team " + msg.team_name + " has found the result!")
                        self.hash_result = curr_hash_result
                        self.found_result = True
                        return False
                    else:
                        print("Team " + msg.team_name + " is on team Cap.")
                elif msg.type == 5:  # NAck
                    self.set_future_nack(address[0], address[1], msg)
                return True
            else:
                return True
        except:
            return True

    def communicate(self, hash, msg_length):
        while len(self.available_servers) == 0:
            self.discover(hash, msg_length)
        self.send_to_servers(hash, msg_length)
        while self.receive_msg(hash):
            if not self.found_result:
                self.timeout_treatment(hash, msg_length)
            else:
                break
        for future_obj in self.futures:
            future_obj.timer.cancel()
        return self.hash_result
