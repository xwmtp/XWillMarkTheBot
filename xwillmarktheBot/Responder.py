from xwillmarktheBot.Config import Configs
from xwillmarktheBot.Commands.Speedrun_stats.SpeedRunsLive.Live_races.Race_handler import Race_handler
from xwillmarktheBot.Commands.Speedrun_stats.Speedrun_handler import Speedrun_handler
from xwillmarktheBot.Commands.Randomizer.Rando_handler import Rando_handler
from xwillmarktheBot.Commands.Other_commands.SRL_setting_commands import SRL_setting_commands
from xwillmarktheBot.Commands.Other_commands.General_commands import General_commands

class Responder:

    def __init__(self):
        self.handlers = []

        self.handlers.append(Speedrun_handler())
        if Configs.get('srl races'):
            self.handlers.append(Race_handler())
        if Configs.get('rando'):
            self.handlers.append(Rando_handler())
        self.handlers.append(General_commands())
        self.handlers.append(SRL_setting_commands())

    def get_response(self, message):
        for handler in self.handlers:
            if handler.triggered(message.content.split(" ")[0]):
                return handler.handle_message(message.content, message.sender)
