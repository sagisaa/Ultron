import sys
from Messages.Imports import *

def main():

    numOfServers = 1
    if len(sys.argv) != 2:
        print "Number of servers set to default: 1"
    else:
        numOfServers = int(sys.argv[1])
        print("Number of servers is set to " + str(numOfServers))


if __name__ == '__main__':
    main()