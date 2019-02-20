from Utils import *

class Message_handler():

    def __init__(self):
        self.commands = {}

    # abstract method
    def handle_message(self, msg, sender):
        raise NotImplementedError('Subclasses must override handle_message()!')

    def get_commands(self):
        if self.commands == {}:
            raise NotImplementedError('Subclasses must have self.commands attribute.')
        return flatten(self.commands.values())