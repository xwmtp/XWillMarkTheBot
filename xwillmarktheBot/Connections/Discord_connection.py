from xwillmarktheBot.Responder import Responder
from xwillmarktheBot.Config import Configs
from xwillmarktheBot.Connections.Message import convert_discord_message
import discord
import logging

def setup_and_run_discord():
    Discord_connection().run()


class Discord_connection:

    def __init__(self):
        self.client = MyClient(Responder())

    def run(self):
        self.client.run(Configs.get('bot_oauth'))


class MyClient(discord.Client):

    def __init__(self, responder):
        super().__init__()
        self.responder = responder

    async def on_ready(self):
        logging.debug(f'Logged on as Discord user {self.user}')

    async def send_message(self, incoming_message, outgoing_message):
        await incoming_message.channel.send(outgoing_message)
        logging.info('Sent message: ' + outgoing_message)

    async def on_message(self, discord_message):
        # don't respond to ourselves
        if discord_message.author == self.user:
            return

        logging.info('Received discord_message: ' + discord_message.content)

        response = self.responder.get_response(convert_discord_message(discord_message))

        # multiple responses
        if isinstance(response, list):
            for discord_message in response:
                return await self.send_message(discord_message, response)

        # 1 response
        if response:
            await self.send_message(discord_message, response)

        if discord_message.content == 'ping':
            await self.send_message(response, 'pong')
