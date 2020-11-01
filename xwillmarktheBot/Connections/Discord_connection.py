from xwillmarktheBot.Bot import Message_distributor
from xwillmarktheBot.Config import Configs
import discord
import logging

class Discord_connection:

    def __init__(self):
        bot = Message_distributor()
        self.client = MyClient(bot)

    def run(self):
        self.client.run(Configs.get('bot_oauth'))

class MyClient(discord.Client):

    def __init__(self, message_handler):
        super().__init__()
        self.message_handler = message_handler

    async def on_ready(self):
        logging.debug(f'Logged on as Discord user {self.user}')

    async def send_message(self, incoming_message, outgoing_message):
        await incoming_message.channel.send(outgoing_message)
        logging.info('Sent message: ' + outgoing_message)

    async def on_message(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        logging.info('Received message: ' + message.content)

        return_message = self.message_handler.get_response(message.content.lower(), message.author.name)

        # multiple messages
        if isinstance(return_message, list):
            for message in return_message:
                return await self.send_message(message, return_message)

        if return_message:
            await self.send_message(message, return_message)

        if message.content == 'ping':
            await self.send_message(message, 'pong')