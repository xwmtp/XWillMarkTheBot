from xwillmarktheBot.Abstract_Message_Handler import Message_handler
from xwillmarktheBot.Settings import Configs, Definitions

class SRL_setting_commands(Message_handler):

    def __init__(self, irc_connection):
        super().__init__(irc_connection)

        self.commands = {
            'set_srl' : ['!setsrl', '!set_srl'],
            'get_srl' : ['!getsrl', '!get_srl']
        }



    def handle_message(self, msg, sender):
        split_msg = msg.lower().split(' ')
        command = split_msg[0]

        for func, command_group in self.commands.items():
            if command in command_group:
                return eval(f'self.{func}("{msg}","{sender}")')


    def set_srl(self, msg, sender):
        if sender in Configs.get('editors'):
            split_msg = msg.lower().split(' ')
            arg = split_msg[1]
            if arg in Definitions.RACE_TYPES:
                Configs.set('default race type', arg)
                self.send(f'Updated default SRL race type to {arg}.')
            else:
                self.send(f"Argument not a valid SRL race type! Choose from: {', '.join(Definitions.RACE_TYPES)}")
        else:
            self.send(f"{sender} does not have the permissions to use this command.")

    def get_srl(self, msg, sender):
        if sender in Configs.get('editors'):
            self.send(f"SRL race type is currently set to {Configs.get('default race type')}.")
        else:
            self.send(f"{sender} does not have the permissions to use this command.")

