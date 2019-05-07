from xwillmarktheBot.Abstract_Message_Handler import Message_handler

class General_commands(Message_handler):

    def __init__(self, irc_connection):
        super().__init__(irc_connection)

        self.commands = {
            'commands_list' : ['!command', '!commands'],
            'repo_link' : ['!bot', '!xwillmarkthebot', '!repo']
        }



    def handle_message(self, msg, sender):
        split_msg = msg.lower().split(' ')
        command = split_msg[0]

        for func, command_group in self.commands.items():
            if command in command_group:
                return eval(f'self.{func}("{msg}","{sender}")')

    def commands_list(self, msg, sender):
        self.send("https://xwmtp.github.io/xwmtp_bot/")

    def repo_link(self, msg, sender):
        self.send('https://github.com/xwmtp/xwillmarktheBot')