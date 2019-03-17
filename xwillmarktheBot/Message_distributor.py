from xwillmarktheBot.Speedrun_com.SRC_handler import SRC_handler
from xwillmarktheBot.SpeedRunsLive.Results.Result_handler import Result_handler
from xwillmarktheBot.SpeedRunsLive.Live_races.Race_handler import Race_handler
from xwillmarktheBot.Randomizer.Rando_handler import Rando_handler
from xwillmarktheBot.Other_commands.Setting_commands import Setting_commands
from xwillmarktheBot.Settings import Settings
import logging


class Message_distributor:

    def __init__(self, irc_connection):
        self.handlers = self.get_handlers(irc_connection)


    def get_handlers(self, irc):
        handlers = []
        if Settings.SPEEDRUN_COM:
            handlers.append(SRC_handler(irc))
        if Settings.SRL_RACES:
            handlers.append(Race_handler(irc))
        if Settings.SRL_RESULTS:
            handlers.append(Result_handler(irc))

        handlers.append(Rando_handler(irc))

        handlers.append(Setting_commands(irc))

        return handlers


    def find_command(self, message, sender):
        """Looks for commands in message to send the command to the right message handler."""
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





