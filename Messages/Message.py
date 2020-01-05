import struct

class Message:

    def __init__(self):
        self.type = 0
        self.hash = ""
        self.origin_length = 0
        self.origin_start = ""
        self.origin_end = ""

    def Init(self):
        raise Exception("This is an abstract message")

    def operate(self):
        raise Exception("This is an abstract message")

    def encodeMyself(self):
        hashUtf8 = self.hash.encode('utf-8')
        originStartUtf8 = self.origin_start.encode('utf-8')
        originEndUtf8 = self.origin_end.encode('utf-8')
        encodedM = struct.pack('B40sB256s256s', self.type, hashUtf8, self.origin_length, originStartUtf8, originEndUtf8)
        return encodedM
