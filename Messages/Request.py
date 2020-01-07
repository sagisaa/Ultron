from Messages.Message import Message

class Request(Message):

    def __init__(self):
        Message.__init__(self)

    def Init(self, hash, origin_length, origin_start, origin_end):
        self.type = 3
        self.hash = hash
        self.origin_length = origin_length
        self.origin_start = origin_start
        self.origin_end = origin_end