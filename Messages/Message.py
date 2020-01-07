class Message:

    def __init__(self):
        self.team_name = "Jarvis"
        self.type = 0
        self.hash = ""
        self.origin_length = 0
        self.origin_start = ""
        self.origin_end = ""

    def Init(self):
        raise Exception("This is an abstract message")
