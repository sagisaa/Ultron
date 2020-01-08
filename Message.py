DISCOVER_CODE = 1
OFFER_CODE = 2
REQUEST_CODE = 3
ACK_CODE = 4
NACK_CODE = 5
SELF_TEAM_NAME = "Friday"

class Message:

    def __init__(self, team_name, type, hash, origin_length, origin_start, origin_end):
        self.team_name = team_name
        self.type = type
        self.hash = hash
        self.origin_length = origin_length
        self.origin_start = origin_start
        self.origin_end = origin_end
