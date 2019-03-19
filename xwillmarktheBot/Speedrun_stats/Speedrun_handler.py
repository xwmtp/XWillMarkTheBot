from xwillmarktheBot.Abstract_Message_Handler import Message_handler
from xwillmarktheBot.Speedrun_stats.SpeedRunsLive.Results.Result_handler import Result_handler
from xwillmarktheBot.Speedrun_stats.Speedrun_com.SRC_handler import SRC_handler
from xwillmarktheBot.Speedrun_stats.Stream_title import get_stream_category
from xwillmarktheBot.Settings import Definitions
from xwillmarktheBot.Utils import *

from xwillmarktheBot.Settings import Settings


class Speedrun_handler(Message_handler):
    """MLayer to send commands to SRL results or SRC. Handles !pb commands differently."""

    def __init__(self, irc_connection):
        super().__init__(irc_connection)

        self.SRC_handler = SRC_handler(irc_connection)
        self.result_handler = Result_handler(irc_connection)

        self.commands = {
            'handle_pb' : ['!pb']
        }

        # add child message handler commands to the command dict
        self.commands = merge_list_dictionaries(self.commands, self.SRC_handler.commands)
        self.commands = merge_list_dictionaries(self.commands, self.result_handler.commands)

    def handle_message(self, msg, sender):
        split_msg = msg.split(' ')
        command = split_msg[0]

        # handle pb separately (can be either results (bingo) or src)
        if command in self.commands['handle_pb']:
            self.handle_pb(msg, sender)

        elif command in self.SRC_handler.get_commands():
            self.SRC_handler.handle_message(msg, sender)
        elif command in self.result_handler.get_commands():
            self.result_handler.handle_message(msg, sender)




    def handle_pb(self, msg, sender):
        """In case of !pb command: decide whether to send to SRL result handler or SRC.
        If there's a race type involved, it goes to SRL."""
        split_msg = msg.split(' ')

        # check in stream title
        if len(split_msg) == 1:
            arg = get_stream_category()
        # argument
        else:
            arg = split_msg[1]

        logging.debug(f"Comparing argument {arg} with race types: {Definitions.RACE_TYPES}")
        if any(type in arg for type in Definitions.RACE_TYPES):
            self.result_handler.handle_message(msg, sender)
        else:
            self.SRC_handler.handle_message(msg, sender)







