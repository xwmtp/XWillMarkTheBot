from xwillmarktheBot.Utils import *

class Message_handler():

    def __init__(self, irc_connection):
        # commands in the class
        self.commands = {}
        # triggers in the class (words anywhere in message that may trigger the bot, like blue tunic)
        self.triggers = {}

        self.irc = irc_connection

    # abstract method
    def handle_message(self, msg, sender):
        raise NotImplementedError('Subclasses must override handle_message()!')


    def send(self, msg):
        self.irc.send_message(msg)

    def get_commands(self):
        if self.commands == {}:
            raise NotImplementedError('Subclasses must have self.commands attribute.')
        return flatten(self.commands.values())

    def get_triggers(self):
        # could possibly be empty, which is fine
        return flatten(self.triggers.values())