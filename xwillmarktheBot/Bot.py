from xwillmarktheBot.Config import Configs
from xwillmarktheBot.Speedrun_stats.SpeedRunsLive.Live_races.Race_handler import Race_handler
from xwillmarktheBot.Speedrun_stats.Speedrun_handler import Speedrun_handler
from xwillmarktheBot.Randomizer.Rando_handler import Rando_handler
from xwillmarktheBot.Other_commands.SRL_setting_commands import SRL_setting_commands
from xwillmarktheBot.Other_commands.General_commands import General_commands
import logging
import re

class Bot:

    def __init__(self, connection):
        self.connection = connection
        self.handlers = []

        self.handlers.append(Speedrun_handler())
        if Configs.get('srl races'):
            self.handlers.append(Race_handler())
        if Configs.get('rando'):
            self.handlers.append(Rando_handler())
        self.handlers.append(General_commands())
        self.handlers.append(SRL_setting_commands())

    def run(self):
        logging.info("Starting bot.")

        while(True):

            irc_message = self.connection.get_next_message()
            if not irc_message:
                continue

            for handler in self.handlers:
                if handler.triggered(irc_message.command.split(" ")[0]):
                    message = Message(irc_message)
                    response = handler.handle_message(message.content, message.sender)
                    self.connection.send_message(response)


class Message:

    def __init__(self, irc_message):
        self.sender = irc_message.sender()
        self.content = irc_message.content
        self.permission = self.get_permission(irc_message.tag)

    def get_permission(self, tag):
        permission = 'viewer'
        if tag is not None:
            match = re.search(r"badges=[^;]*;", self.content)
            if match:
                badges = match.group()
                for permission in ['broadcaster', 'moderator', 'subscriber']:
                    if permission in badges:
                        return permission
        return permission
