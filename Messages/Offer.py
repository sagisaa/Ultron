from Messages.Message import *

class Offer(Message):

    def __init__(self):
        Message.__init__(self)

    def Init(self, hash, origin_length, origin_input):
        self.type = 2
        self.hash = ""
        self.origin_length = 0
        self.origin_start = ""
        self.origin_end = ""

    def operate(self):
        print("mkl")