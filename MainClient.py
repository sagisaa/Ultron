from Client import *


def main():
    stop = False
    while not stop:
        print "At your service sir."
        hashing = raw_input("What hashing message do you want to decrypt?\n")
        hashing_length = raw_input("Sir, what is the length of the original message? ")
        print "Thank you sir, my resources are now calculating the data for you."

        client = Client()
        client.communicate(hashing, hashing_length)


if __name__ == '__main__':
    main()