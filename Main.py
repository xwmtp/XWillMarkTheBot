from Message_handler import *

if __name__ == '__main__':
    message_handler = Message_handler()

    #message = input("Chat message:").lower()
    message = "!pb mweep%"

    while(True):
        message_handler.find_command(message)
        message = input().lower()
