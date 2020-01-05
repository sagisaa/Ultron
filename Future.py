import threading
from Messages.Message import *
TRESHOLD_SERVER_DELAY = 15.0


class Future:

    def __init__(self):
        self.string_range = []                 # (start_string, end_string)
        self.server = []                # (server_ip, server_port)
        self.timer = None               # thread timer
        self.answer = Message()              # message - Ack/NAck
        self.timeout = False

    def set_timeout(self):
        self.timeout = True

    def is_timeout(self):
        return self.timeout

    def start_timer(self):
        self.timeout = False
        self.timer.start()

    def Init(self, string_range, server):
        self.string_range = string_range
        self.server = server
        self.timer = threading.Timer(TRESHOLD_SERVER_DELAY, self.set_timeout)
        self.answer = None

    def update_answer(self, result):
        self.timeout = False
        self.answer = result
