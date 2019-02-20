from Utils import *
import random

STREAMER = 'xwillmarktheplace'

class Simple_commands():

    def __init__(self):
        self.monka_emotes = []

    def monka(self, msg):
        if self.monka_emotes == []:
            url = "https://api.frankerfacez.com/v1/room/" + STREAMER
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