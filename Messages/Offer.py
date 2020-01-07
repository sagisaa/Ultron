from Messages.Message import *

class Offer(Message):

    def __init__(self):
        Message.__init__(self)

    def Init(self):
        self.type = 2
        self.hash = ""
        self.origin_length = 0
        self.origin_start = ""
        self.origin_end = ""