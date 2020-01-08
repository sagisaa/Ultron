from Client import *
from Message import *
import sys

def main():
    # stop = False
    while True:
        print "Jarvis is at your service sir."
        hashing = raw_input("What hashing message do you want to decrypt?\n")
        hashing_length = int(raw_input("Sir, what is the length of the original message? "))
        print "Thank you sir, my resources are now calculating the data for you."
        client = Client()
        result = client.communicate(hashing, hashing_length)
        if result == "":
            print("I'm sorry sir, but there is no result for the requested hash.")
            exit(0)
        else:
            print("The input for " + hashing + " is: " + result)
        sys.exit(0)


if __name__ == '__main__':
    main()