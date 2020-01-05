import sys
from Messages.Imports import *
import Client


def num_to_word(num, len):
    letters = "abcdefghijklmnopqrstuvwxyz"
    remainder = num % 26
    rest = num / 26
    last_letter = letters[remainder]
    if len > 1:
        return num_to_word(rest, len - 1) + last_letter
    else:
        return last_letter

def divide_range(msg_length):
    #### return array of pairs
    pairs = []
    start = 0
    end = 26 ** msg_length
    rng = (end / 4.0)
    for i in range(0, 4):
        pairs.append((num_to_word(int(i*rng), msg_length), num_to_word(int((i+1)*rng)-1, msg_length)))
    return pairs

def main():

    print divide_range(8)


    numOfServers = 1
    if len(sys.argv) != 2:
        print "Number of servers set to default: 1"
    else:
        numOfServers = int(sys.argv[1])
        print("Number of servers is set to " + str(numOfServers))


if __name__ == '__main__':
    main()
