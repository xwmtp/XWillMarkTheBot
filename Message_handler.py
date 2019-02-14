from SRC.SRC_handler import SRC_handler
from Bingo.Bingo_handler import Bingo_handler
from Utils import Database

class Message_handler:

    def __init__(self):
        self.SRC_handler = SRC_handler()
        self.Bingo_handler = Bingo_handler()
        self.command_base = Database()
        self.command_base[('!pb', '!userpb', '!wr')] = self.SRC_handler.handle_SRC_message
        self.command_base[('!average', '!mean', '!median', '!results')] = self.Bingo_handler.handle_bingo_message


    def find_command(self, message):
        m = message.lower().split(' ')[0]


        self.command_base.keys()


        for commands, method in self.command_base.items():
            if m in commands:
                method()




