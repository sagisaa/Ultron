from Client import *
from Message import *
import sys

def main():
    # stop = False
    # while not stop:
        # print "Jarvis is at your service sir."
        # hashing = raw_input("What hashing message do you want to decrypt?\n")
        # hashing_length = int(raw_input("Sir, what is the length of the original message? "))
        # print "Thank you sir, my resources are now calculating the data for you."
    hashing = "9017347a610d1436c1aaf52764e6578e8fc1a083" #cyber
    hashing_length = 5
    client = Client()
    result = client.communicate(hashing, hashing_length)
    print(SELF_TEAM_NAME + " has done calculating.")
    print("The input for " + hashing + " is: " + result)
    sys.exit(0)


if __name__ == '__main__':
    main()