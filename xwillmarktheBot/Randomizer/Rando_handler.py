from xwillmarktheBot.Abstract_Message_Handler import Message_handler
from xwillmarktheBot.Randomizer.Hints import send_current_hints, reset_hints
from xwillmarktheBot.Settings import Settings

class Rando_handler(Message_handler):

    def __init__(self):
        super().__init__()

        self.commands = {
            'hints' : ['!hints', '!randohints', '!randohint', '!hint'],
            'reset_hints' : ['!resethints', '!resethint']
        }


    def handle_message(self, msg, sender):
        split_msg = msg.lower().split(' ')
        command = split_msg[0]

        if command in self.commands['hints']:
            return self.hints()

        if command in self.commands['reset_hints']:
            return self.reset_hints(sender)



    def hints(self):
        to_send = send_current_hints()
        if to_send:
            return to_send
        elif to_send == []:
            return "No hints found yet."
        else:
            return "Hints couldn't be read."


    def reset_hints(self, sender):
        if sender in Settings.EDITORS:
            if reset_hints():
                return "Hints file reset to default."
            else:
                return "Hints couldn't be reset."
        else:
            return sender + "does not have the rights to use this command."











