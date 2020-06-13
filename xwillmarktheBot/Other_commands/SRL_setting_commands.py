from xwillmarktheBot.Abstract_Message_Handler import Message_handler
from xwillmarktheBot.Config import Configs, Definitions

class SRL_setting_commands(Message_handler):

    def __init__(self):
        super().__init__()

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
                return f'Updated default SRL race type to {arg}.'
            else:
                return f"Argument not a valid SRL race type! Choose from: {', '.join(Definitions.RACE_TYPES)}"
        else:
            return f"{sender} does not have the permissions to use this command."

    def get_srl(self, msg, sender):
        if sender in Configs.get('editors'):
            return f"SRL race type is currently set to {Configs.get('default race type')}."
        else:
            return f"{sender} does not have the permissions to use this command."

