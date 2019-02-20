from SRC.SRC_handler import SRC_handler
from Bingo.Bingo_handler import Bingo_handler
from Simple_commands import Simple_commands
from Utils import *

class Message_handler:

    def __init__(self):
        self.SRC_handler = SRC_handler()
        self.Bingo_handler = Bingo_handler()
        self.Simple_commands = Simple_commands()

        self.commands_dictionary = {
            self.SRC_handler.handle_SRC_message     : ['!pb', '!userpb', '!wr'],
            self.Bingo_handler.handle_bingo_message : ['!average', '!mean', '!median', '!results'],
            self.Simple_commands.monka              : ['!monka', '!monkas'],
        }

        self.commands_dictionary = reverse_dictionary(self.commands_dictionary)


    def find_command(self, message):
        m = message.split(' ')[0]


        for command, function in self.commands_dictionary.items():

            if m in command:
                function(message)
                return





