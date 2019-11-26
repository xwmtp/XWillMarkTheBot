from xwillmarktheBot.Abstract_Message_Handler import Message_handler
from xwillmarktheBot.Utils import *
from xwillmarktheBot.Settings import Configs

import random

class xwmtp_commands(Message_handler):

    def __init__(self):
        super().__init__()
        self.monka_emotes = []

        self.commands = {
            'monka' : ['!monkas', '!monka'],
            'social': ['!social', '!discord', '!twitter', '!socialmedia']
        }

        self.triggers = {
            'tunic'  : ['zora tunic', 'blue tunic', 'blauwe tuniek', 'zora tuniek', 'tunique bleu', 'blaue tunika']
        }

    def handle_message(self, msg, sender):
        split_msg = msg.lower().split(' ')
        command = split_msg[0]

        for func, command_group in self.commands.items():
            if command in command_group:
                return eval(f'self.{func}("{command}")')

        for func, triggers in self.triggers.items():
            if  any([tr for tr in triggers if tr in msg]):
                return eval(f'self.{func}("{msg}")')


    def monka(self, command):
        if self.monka_emotes == []:
            url = "https://api.frankerfacez.com/v1/room/" + Configs.get('streamer')
            json = readjson(url)
            emotes = json['sets']['164185']['emoticons']

            monka_emotes = []
            for emote in emotes:
                emote_name = emote['name']
                if 'monka' in emote_name:
                    monka_emotes.append(emote_name)
            self.monka_emotes = monka_emotes
        else:
            monka_emotes = self.monka_emotes
        return random.choice(monka_emotes)



    # Post badTunic
    def tunic(self, msg):
        return 'BadTunic'



    def social(self, command):
        socials = {
            'discord' : "Join my Discord: https://discord.gg/DuayYUV",
            'twitter' : "Follow me on Twitter: https://twitter.com/xwmtp"
        }

        # send just one social link (if found in message command)
        for social, link in socials.items():
            if social in command:
                return link

        # send all social links
        return ' '.join(socials.values())