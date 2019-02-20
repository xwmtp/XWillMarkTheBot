from Message_handlers.SRC.SRC_handler import SRC_handler
from Message_handlers.Bingo.Bingo_handler import Bingo_handler
from Message_handlers.SRL_races.Race_handler import Race_handler
from Simple_commands import Simple_commands
from Utils import *
import Settings

class Chatbot:

    def __init__(self):
        self.handlers = [Race_handler(), Bingo_handler(), SRC_handler(), Simple_commands()]


    def find_command(self, message):
        m = message.split(' ')[0]

        for handler in self.handlers:
            if m in handler.get_commands():
                handler.handle_message(message, Settings.STREAMER)





