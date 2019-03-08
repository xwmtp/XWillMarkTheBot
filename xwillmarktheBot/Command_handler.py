from xwillmarktheBot.Message_handlers.SRC.SRC_handler import SRC_handler
from xwillmarktheBot.Message_handlers.Bingo.Bingo_handler import Bingo_handler
from xwillmarktheBot.Message_handlers.SRL_races.Race_handler import Race_handler
from xwillmarktheBot.Message_handlers.Simple_commands import Simple_commands
from xwillmarktheBot import Settings
import logging


class Command_handler:

    def __init__(self, irc_connection):
        self.handlers = [Race_handler(irc_connection),
                         Bingo_handler(irc_connection),
                         SRC_handler(irc_connection),
                         Simple_commands(irc_connection)]


    def find_command(self, message, sender):
        command = message.split(' ')[0]
        msg = message

        # exact match
        for handler in self.handlers:
            trigger_matches = [tr for tr in handler.get_triggers() if tr in msg]

            if (command in handler.get_commands()) | any(trigger_matches):
                logging.debug('found')
                return handler.handle_message(message, sender)


        # starts with
        for handler in self.handlers:
            for command in handler.get_commands():
                if msg.startswith(command):
                    return handler.handle_message(message, sender)





