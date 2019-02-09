from SRC import *

class Message_handler:

    def __init__(self):
        self.SRC_handler = SRC_handler()

    def find_command(self, message):
        m = message.lower().split(' ')[0]
        if m == "!pb" or m == "!wr" or m == "!userpb":
            self.SRC_handler.handle_SRC_message(message)



