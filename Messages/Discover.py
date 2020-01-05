from Messages.Message import *

class Discover(Message):

    def __init__(self):
        Message.__init__(self)

    def Init(self):
        self.type = 1
        self.hash = ""
        self.origin_length = 0
        self.origin_start = ""
        self.origin_end = ""

    def operate(self):
        print("mkl")