from xwillmarktheBot.Message_distributor import Message_distributor
from xwillmarktheBot.Config import Configs
import discord
import logging



class Discord_messages:

    def __init__(self):
        bot = Message_distributor()
        self.client = MyClient(bot)

    def run(self):
        self.client.run(Configs.get('bot_oath'))




class MyClient(discord.Client):

    def __init__(self, message_handler):
        super().__init__()
        self.message_handler = message_handler


    async def on_ready(self):
        print('Logged on as', self.user)

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


        # roles
        if message.content.startswith('!add') or message.content.startswith('!remove'):
            words = message.content.split(' ')
            command = words[0]
            if len(words) <= 1:
                await self.send_message(message, 'Please supply a notification role.')
            else:
                roles = message.guild.roles
                bot_role = message.guild.get_member(self.user.id).top_role
                available_roles   = [str(role)         for role in roles if role <  bot_role and str(role) != '@everyone']
                unavailable_roles = [str(role).lower() for role in roles if role >= bot_role]

                for word in words[1:]:
                    if word.lower() in unavailable_roles:
                        kappa = discord.utils.get(message.guild.emojis, name='Kappa')
                        await self.send_message(message, 'Nice try ' + str(kappa))
                        continue


                    role = discord.utils.get(message.guild.roles, name=word.lower())

                    if role:
                        try:
                            if command == '!add':
                                await message.author.add_roles(role)
                                await self.send_message(message, "Added role '" + str(role) + "'.")
                            if command == '!remove':
                                await message.author.remove_roles(role)
                                await self.send_message(message, "Removed role '" + str(role) + "'.")
                        except discord.errors.Forbidden:
                            kappa = discord.utils.get(message.guild.emojis, name='Kappa')
                            await self.send_message(message, 'Nice try ' + str(kappa))

                    else:
                        await self.send_message(message, 'Incorrect role. Available notification roles are: ' + ', '.join(available_roles))