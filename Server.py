import threading
import socket
import EncoderDecoder
import Hash
from Message import *

server_addr = ('', 3117)
BUFFER_SIZE = 586
lock_obj = threading.Lock()

class Server:

    def __init__(self):
        self.server_socket = socket.socket(socket.AF_INET,
                                           socket.SOCK_DGRAM)

    def send_offer(self, client_address, team_name):
        msg = Message(SELF_TEAM_NAME, OFFER_CODE, "", 0, "", "")
        print("Jarvis is offering service to team " + team_name + ", address: " + str(client_address))
        self.server_socket.sendto(EncoderDecoder.encodeMessage(msg), client_address)

    def start(self):
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.server_socket.bind(server_addr)

        while True:

            # before doing the functionality below, move on the list and remove any thread that has finished
            data, address = self.server_socket.recvfrom(BUFFER_SIZE)
            msg = EncoderDecoder.decodeMessage(data)

            if msg.type == 1:           # Discover
                self.send_offer(address, msg.team_name)

            elif msg.type == 3:         # Request
                print("Received a request from team " + msg.team_name + ", address: " + str(address) + " with range (" + msg.origin_start + ", " + msg.origin_end + ")")
                # curr_thread_per_client = [address, None, ""]
                client_thread = threading.Thread(target=Hash.calc_hash,
                                                 args=(msg, self.server_socket,
                                                       address, lock_obj))
                # curr_thread_per_client[1] = client_thread
                client_thread.start()
