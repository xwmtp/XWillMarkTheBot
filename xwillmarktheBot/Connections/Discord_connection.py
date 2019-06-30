from xwillmarktheBot.Message_distributor import Message_distributor
import discord
import logging



class Discord_messages:

    def __init__(self):
        bot = Message_distributor('')
        self.client = MyClient(bot)

    def run(self, token):
        self.client.run(token)




class MyClient(discord.Client):

    def __init__(self, message_handler):
        super().__init__()
        self.message_handler = message_handler


    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        return_message = self.message_handler.find_command(message.content.lower(), message.author)
        logging.debug('Message to send: ' + return_message)
        if return_message:
            await message.channel.send(return_message)

        if message.content == 'ping':
            await message.channel.send('pong')

