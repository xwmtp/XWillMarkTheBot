from Message_handlers.Message_handler import Message_handler
from Utils import *
import Settings

import random

class Simple_commands(Message_handler):

    def __init__(self):
        self.monka_emotes = []

        self.commands = {
            'monka' : ['!monkas', '!monka']
        }

    def handle_message(self, msg, sender):
        split_msg = msg.lower().split(' ')
        command = split_msg[0]

        if command in self.commands['monka']:
            self.monka(msg)

    def monka(self, msg):
        if self.monka_emotes == []:
            url = "https://api.frankerfacez.com/v1/room/" + Settings.STREAMER
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
        print(random.choice(monka_emotes))



    # Post badTunic
    def tunic(data, msg):
        print("BadTunic")