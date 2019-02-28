from Message_handlers.SRC.SRC_handler import SRC_handler
from Message_handlers.Bingo.Bingo_handler import Bingo_handler
from Message_handlers.SRL_races.Race_handler import Race_handler
from Message_handlers.Simple_commands import Simple_commands
from xwillmarktheBot import Settings


class Chatbot:

    def __init__(self):
        self.handlers = [Race_handler(), Bingo_handler(), SRC_handler(), Simple_commands()]


    def find_command(self, message):
        m = message.split(' ')[0]

        # exact match
        for handler in self.handlers:
            if m in handler.get_commands():
                return handler.handle_message(message, Settings.STREAMER)

        # starts with
        for handler in self.handlers:
            for command in handler.get_commands():
                if m.startswith(command):
                    return handler.handle_message(message, Settings.STREAMER)

        # command present in message (no '!' commands)
        for handler in self.handlers:
            for command in handler.get_commands():
                if (command[0] != '!') & (command in message):
                    return handler.handle_message(message, Settings.STREAMER)





