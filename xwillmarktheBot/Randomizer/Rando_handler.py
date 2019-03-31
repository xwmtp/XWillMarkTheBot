from xwillmarktheBot.Abstract_Message_Handler import Message_handler
from xwillmarktheBot.Randomizer.Hints import send_current_hints, reset_hints
from xwillmarktheBot.Settings import Settings

class Rando_handler(Message_handler):

    def __init__(self, irc_connection):
        super().__init__(irc_connection)

        self.commands = {
            'hints' : ['!hints', '!hint'],
            'reset_hints' : ['!resethints', '!resethint']
        }


    def handle_message(self, msg, sender):
        split_msg = msg.lower().split(' ')
        command = split_msg[0]

        if command in self.commands['hints']:
            self.hints()

        if command in self.commands['reset_hints']:
            self.reset_hints(sender)



    def hints(self):
        to_send = send_current_hints()
        print(to_send)
        if to_send:
            for hint in to_send:
                self.send(hint)
        elif to_send == []:
            self.send("No hints found yet.")
        else:
            self.send("Hints couldn't be read.")


    def reset_hints(self, sender):
        if sender in Settings.EDITORS:
            if reset_hints():
                self.send("Hints file reset to default.")
            else:
                self.send("Hints couldn't be reset.")
        else:
            self.send(sender + "does not have the rights to use this command.")











