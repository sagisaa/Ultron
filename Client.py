import socket
import threading
from Messages.Imports import *

server_port = 3117
IP_broadcast = "255.255.255.255"
BUFFER_SIZE = 586

class Client:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receiving_buffer = []
        self.sending_buffer = []
        self.connected_servers = []
        self.listen = True

    def stop_listening(self):
        self.listen = False

    def start_listening(self):
        self.listen = True

    def connect_to_server(self, server):
        self.connected_servers.append(server)

    def disconnect_from_server(self, server):
        self.connected_servers.remove(server)

    def discover(self):
        discover_message = Discover()
        self.client_socket.sendto(discover_message.encodeMyself(), (IP_broadcast, server_port))
        time_out = threading.Timer(1.0, self.stop_listening)
        time_out.start()

        while self.listen:
            msg, address = self.client_socket.recv(BUFFER_SIZE)
            ### convert msg to Offer and check valid
            self.connect_to_server(address)

    def divide_range(self, msg_length):
        #### return array of pairs
        return []

    def send_to_servers(self, ):
        return -1

    def communicate(self, hash, length):
        self.discover()
