import sys
from Messages.Imports import *
import EncoderDecoder

def main():

    numOfServers = 1
    if len(sys.argv) != 2:
        print("Number of servers set to default: 1")
    else:
        numOfServers = int(sys.argv[1])
        print("Number of servers is set to " + str(numOfServers))

    msg = Request()
    msg.Init("hashash", 4, "a", "b")
    v = EncoderDecoder.encodeMessage(msg)
    p = EncoderDecoder.decodeMessage(v)
    print("stop for debug")

if __name__ == '__main__':
    main()