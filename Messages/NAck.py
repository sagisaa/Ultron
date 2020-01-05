from Message import *

class NAck(Message):

    def __init__(self):
        Message.__init__(self)

    def Init(self, hash, origin_length):
        self.type = 5
        self.hash = hash
        self.origin_length = origin_length
        self.origin_start = ""
        self.origin_end = ""

    def operate(self):
        print("mkl")