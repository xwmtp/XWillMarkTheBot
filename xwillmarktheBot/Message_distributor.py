from xwillmarktheBot.Speedrun_stats.SpeedRunsLive.Live_races.Race_handler import Race_handler
from xwillmarktheBot.Speedrun_stats.Speedrun_handler import Speedrun_handler
from xwillmarktheBot.Randomizer.Rando_handler import Rando_handler
from xwillmarktheBot.Other_commands.SRL_setting_commands import SRL_setting_commands
from xwillmarktheBot.Other_commands.General_commands import General_commands
from xwillmarktheBot.Settings import Configs
import logging


class Message_distributor:

    def __init__(self):
        self.handlers = self.get_handlers()


    def get_handlers(self):
        handlers = []

        handlers.append(Speedrun_handler())
        if Configs.get('srl races'):
            handlers.append(Race_handler())


        if Configs.get('rando'):
            handlers.append(Rando_handler())

        if Configs.get('general'):
            handlers.append(General_commands())
        handlers.append(SRL_setting_commands())

        return handlers


    def get_response(self, message, sender):
        """Looks for commands in message and returns a response if a command is triggered"""
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





