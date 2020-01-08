import threading
from Message import *
TRESHOLD_SERVER_DELAY = 30.0


class Future:

    def __init__(self):
        self.string_range = []                 # (start_string, end_string)
        self.server = []                # (server_ip, server_port)
        self.timer = None               # thread timer
        self.answer = Message(SELF_TEAM_NAME, 0, "", 0, "", "")
        self.timeout = False

    def set_timeout(self):
        self.timeout = True

    def is_timeout(self):
        return self.timeout

    def start_timer(self):
        self.timer = threading.Timer(TRESHOLD_SERVER_DELAY, self.set_timeout)
        self.timeout = False
        self.timer.start()

    def Init(self, string_range, server):
        self.string_range = string_range
        self.server = server
        self.timer = threading.Timer(TRESHOLD_SERVER_DELAY, self.set_timeout)
        self.answer = Message(SELF_TEAM_NAME, 0, "", 0, "", "")

    def update_answer(self, result):
        self.timeout = False
        self.answer = result
