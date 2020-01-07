from Messages.Message import *

class Ack(Message):

    def __init__(self):
        Message.__init__(self)

    def Init(self, hash, origin_length, origin_input):
        self.type = 4
        self.hash = hash
        self.origin_length = origin_length
        self.origin_start = origin_input
        self.origin_end = ""
