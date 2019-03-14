from xwillmarktheBot.Abstract_Message_Handler import Message_handler
from xwillmarktheBot.Randomizer.Hints import send_current_hints, reset_hints

class Rando_handler(Message_handler):

    def __init__(self, irc_connection):
        super().__init__(irc_connection)

        self.commands = {
            'hints' : ['!hints', '!hint'],
        }


    def handle_message(self, msg, sender):
        split_msg = msg.lower().split(' ')
        command = split_msg[0]

        if command in self.commands['hints']:
            self.send_current_hints()








