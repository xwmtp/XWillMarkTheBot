from xwillmarktheBot.Message_handlers.Message_handler import Message_handler
from xwillmarktheBot.Utils import *
from xwillmarktheBot import Settings

import random

class Simple_commands(Message_handler):

    def __init__(self, irc_connection):
        super().__init__(irc_connection)
        self.monka_emotes = []

        self.commands = {
            'monka' : ['!monkas', '!monka'],
            'tunic' : ['zora tunic', 'blue tunic', 'blauwe tuniek', 'zora tuniek', 'tunique bleu', 'blaue tunika']
        }

    def handle_message(self, msg, sender):
        split_msg = msg.lower().split(' ')
        command = split_msg[0]

        if command in self.commands['monka']:
            return self.monka()

        for command in self.commands['tunic']:
            if command in msg:
                return self.tunic()

    def monka(self):
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
        self.send(random.choice(monka_emotes))



    # Post badTunic
    def tunic(self):
        self.send("BadTunic")