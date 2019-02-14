from Message_handler import *
import logging

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    message_handler = Message_handler()

    #message = input("Chat message:").lower()
    message = "!average"

    while(True):
        message_handler.find_command(message)
        message = input().lower()
