from xwillmarktheBot.Message_handlers.Message_handler import Message_handler
from xwillmarktheBot.Utils import *
from xwillmarktheBot import Settings
import json as json_module

class Race_handler(Message_handler):

    def __init__(self, irc_connection):
        super().__init__(irc_connection)
        self.race = Current_race(irc_connection)

        self.commands = {
            'race' : ['!race'],
            'card' : ['!card', '!board', '!chart'],
            'goal' : ['!goal'],
            'id'   : ['#srl']
        }


    def handle_message(self, msg, sender):
        split_msg = msg.lower().split(' ')
        command = split_msg[0]

        if command.startswith('#srl'):
            self.race.set(command, sender)
        elif self.race.race_id == '':
            self.send("No SRL race set yet!")
        elif command in self.commands['race']:
            self.race.send_info()
        elif command in self.commands['goal']:
            self.race.send_goal()
        elif command in self.commands['card']:
            self.race.send_card()

    def get_commands(self):
        return flatten(self.commands.values())





class Current_race:

    def __init__(self, irc_connection):
        self.goal = ''
        self.race_id = ''
        self.irc = irc_connection


    def set(self, msg, sender):
        if sender in Settings.EDITORS:
            race_id = msg.replace('#srl-', '')

            self.race_id = race_id

            self.irc.send_message(f"The !race command has been updated (#srl-{race_id}).")
            self.send_info()


    def send_info(self):
        if self._update():

            url = 'http://www.speedrunslive.com/race/?id=' + self.race_id
            entrants = ', '.join([e.get_string() for e in self.entrants])

            self.irc.send_message(f"Goal: {self.goal}, SRL link: {url} Entrants: {entrants}")


    def goal_string(self):
        if self._update():
            return self.goal


    def card_string(self):
        if self._update():
            if self.goal.startswith('http://www.speedrunslive.com/tools/oot-bingo'):
                self.irc.send_message(self.goal)
            else:
                self.irc.send_message("Current race not recognized as bingo race. Use !goal to see the goal.")


    def _update(self):
        text = readjson(f"http://api.speedrunslive.com/races/{self.race_id}?callback=renderEntrants", text_only=True)
        # fix invalid json format
        text = text.replace('renderEntrants(', '')
        text = text.replace('})', '}')
        json = json_module.loads(text)

        if not json:
            return self.send(f"No SRL race found for current race id #srl-{self.race_id}")

        self.goal = json['goal']
        self.entrants = self.get_entrants(json)
        return True


    def get_entrants(self, json):
        entrants = []
        for entrant in json['entrants'].values():
            entrants.append(Entrant(entrant))

        return entrants




class Entrant:

    def __init__(self, json):
        self.name = json['displayname']
        self.trueskill = json['trueskill']
        self.rank = json['place']
        self.time = json['time']
        self.comment = json['message']

    def get_string(self):
        return f"{self.name} ({self.trueskill})"



