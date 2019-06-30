from xwillmarktheBot.Message_distributor import Message_distributor
import discord
import logging



class Discord_messages:

    def __init__(self):
        bot = Message_distributor()
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

        return_message = self.message_handler.find_command(message.content.lower(), message.author.name)

        # multiple messages
        if isinstance(return_message, list):
            for message in return_message:
                await message.channel.send(message)

        if return_message:
            await message.channel.send(return_message)

        if message.content == 'ping':
            await message.channel.send('pong')



        if message.content.startswith('!add') or message.content.startswith('!remove'):
            words = message.content.split(' ')
            command = words[0]
            if len(words) <= 1:
                await message.channel.send('Please supply a notification role.')
            else:
                for word in words[1:]:
                    role = discord.utils.get(message.guild.roles, name=word.lower())
                    if role:
                        try:
                            if command == '!add':
                                await message.author.add_roles(role)
                                await message.channel.send("Added role '" + str(role) + "'.")
                            if command == '!remove':
                                await message.author.remove_roles(role)
                                await message.channel.send("Removed role '" + str(role) + "'.")
                        except discord.errors.Forbidden:
                            kappa = discord.utils.get(message.guild.emojis, name='Kappa')
                            await message.channel.send('Nice try ' + str(kappa))
                    else:
                        await message.channel.send('Incorrect role. Available notification roles are: stream, bingo')