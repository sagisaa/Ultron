import threading
import socket
import EncoderDecoder
import Hash
from Messages.Offer import *

server_addr = ('', 3117)
BUFFER_SIZE = 586
lock_obj = threading.Lock()

class Server:

    def __init__(self):
        # The following field is list of 3 elements.
        # The first element is each pair is a client address,
        # for example: 127.0.0.1, 80
        # The second element is thread which running the analysis
        # process with the client input.
        # The third element is the result
        # self.thread_per_client = []
        self.server_socket = socket.socket(socket.AF_INET,
                                           socket.SOCK_DGRAM)
        # (Client, result To send)
        # self.results_to_send = []

    def send_offer(self, client_address):
        msg = Offer()
        msg.Init()
        print("Offering!")
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
                self.send_offer(address)

            elif msg.type == 3:         # Request
                print("Received a request from: " + str(address))
                # curr_thread_per_client = [address, None, ""]
                client_thread = threading.Thread(target=Hash.calc_hash,
                                                 args=(msg, self.server_socket,
                                                       address, lock_obj))
                # curr_thread_per_client[1] = client_thread
                client_thread.start()
