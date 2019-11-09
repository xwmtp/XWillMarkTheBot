from xwillmarktheBot.Speedrun_stats.SpeedRunsLive.Live_races.Race_handler import Race_handler
from xwillmarktheBot.Speedrun_stats.Speedrun_handler import Speedrun_handler
from xwillmarktheBot.Randomizer.Rando_handler import Rando_handler
from xwillmarktheBot.Other_commands.SRL_setting_commands import SRL_setting_commands
from xwillmarktheBot.Other_commands.General_commands import General_commands
from xwillmarktheBot.Other_commands.xwmtp_commands import xwmtp_commands
from xwillmarktheBot.Settings import Configs
import logging


class Message_distributor:

    def __init__(self, irc_connection):
        self.handlers = self.get_handlers(irc_connection)


    def get_handlers(self, irc):
        handlers = []

        handlers.append(Speedrun_handler(irc))
        if Configs.get('srl races'):
            handlers.append(Race_handler(irc))


        if Configs.get('rando'):
            handlers.append(Rando_handler(irc))

        handlers.append(General_commands(irc))
        handlers.append(SRL_setting_commands(irc))
        handlers.append(xwmtp_commands(irc))

        return handlers


    def find_command(self, message, sender):
        """Looks for commands in message to send the command to the right message handler."""
        command = message.split(' ')[0]
        msg = message

        # exact match
        for handler in self.handlers:
            trigger_matches = [tr for tr in handler.get_triggers() if tr in msg]

            if (command in handler.get_commands()) | any(trigger_matches):
                return handler.handle_message(message, sender)


        # starts with
        for handler in self.handlers:
            for command in handler.get_commands():
                if msg.startswith(command):
                    return handler.handle_message(message, sender)





