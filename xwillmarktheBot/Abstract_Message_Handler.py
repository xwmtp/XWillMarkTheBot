from xwillmarktheBot.Utils import *

class Message_handler():
    """Abstract class defining a general message handler."""

    def __init__(self, irc_connection):
        # commands in the class
        self.commands = {}
        # triggers in the class (words anywhere in message that may trigger the bot, like blue tunic)
        self.triggers = {}

        self.irc = irc_connection

    def handle_message(self, msg, sender):
        """Abstract method. Each message handler has to implement a way to handle incoming messages."""
        raise NotImplementedError('Subclasses must override handle_message()!')


    def send(self, msg):
        """Sending a message to irc."""
        self.irc.send_message(msg)

    def get_commands(self):
        """
        Get all the commands of this class, including aliases.
        Each message handler has to define commands, otherwise an error will be raised.
        """
        if self.commands == {}:
            raise NotImplementedError('Subclasses must have self.commands attribute.')
        return flatten(self.commands.values())

    def get_triggers(self):
        """Get all the trigger of this class, including aliases. Won't throw error if no triggers present."""
        return flatten(self.triggers.values())