import threading
import socket
import EncoderDecoder

SERVER_IP = "127.0.0.1"
SERVER_LISTENING_PORT = 3117

class Server:

    def __init__(self):
        # The following field is list of pairs.
        # The first element is each pair is a client address,
        # for example: 127.0.0.1, 80
        # The second element is thread which running the analysis
        # process with the client input.
        self.thread_per_client = []
        self.server_socket = socket.socket(socket.AF_INET,
                                           socket.SOCK_DGRAM)
        self.server_port = 10000

    def start(self):

        self.server_socket.bind(SERVER_IP, self.server_port)

        while True:
            data, address = self.server_socket.recvfrom(SERVER_LISTENING_PORT)
            msg = EncoderDecoder.decodeMessage(data)
