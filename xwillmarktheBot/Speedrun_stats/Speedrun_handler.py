from xwillmarktheBot.Abstract_Message_Handler import Message_handler
from xwillmarktheBot.Speedrun_stats.SpeedRunsLive.Results.Result_handler import Result_handler
from xwillmarktheBot.Speedrun_stats.Speedrun_com.SRC_handler import SRC_handler
from xwillmarktheBot.Speedrun_stats.Stream_title import get_stream_category
from xwillmarktheBot.Settings import Configs, Definitions
from xwillmarktheBot.Utils import *

class Speedrun_handler(Message_handler):
    """Middle Layer to send commands to SRL results or SRC. Handles !pb commands differently."""

    def __init__(self):
        super().__init__()

        self.SRC_handler = SRC_handler()
        self.result_handler = Result_handler()

        self.commands = {
            'handle_pb' : ['!pb', '!userpb']
        }

        # add child message handler commands to the command dict
        self.commands = merge_list_dictionaries(self.commands, self.SRC_handler.commands)
        self.commands = merge_list_dictionaries(self.commands, self.result_handler.commands)

    def handle_message(self, msg, sender):
        split_msg = msg.split(' ')
        command = split_msg[0]

        # handle pb separately (can be either results (bingo) or src)
        if command in self.commands['handle_pb']:
            return self.handle_pb(msg, sender)

        elif Configs.get('speedrun.com') and command in self.SRC_handler.get_commands():
            return self.SRC_handler.handle_message(msg, sender)
        elif Configs.get('srl results') and command in self.result_handler.get_commands():
            return self.result_handler.handle_message(msg, sender)




    def handle_pb(self, msg, sender):
        """In case of !pb command: decide whether to send to SRL result handler or SRC.
        If there's a race type involved, it goes to SRL."""
        split_msg = msg.split(' ')
        command = split_msg[0]

        num_args = 1
        if command == '!userpb':
            num_args = 2

        # check in stream title
        if len(split_msg) <= num_args:
            arg = get_stream_category()
        # argument
        else:
            arg = ' '.join(split_msg[1:])

        logging.debug(f"Comparing argument '{arg}' to race types: {Definitions.RACE_TYPES}")
        if any(type in arg for type in Definitions.RACE_TYPES):
            if Configs.get('srl results'):
                return self.result_handler.handle_message(msg, sender)

        if Configs.get('speedrun.com'):
            return self.SRC_handler.handle_message(msg, sender)







