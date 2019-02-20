from Message_handlers.Message_handler import Message_handler
import Settings
from Utils import *

class Race_handler(Message_handler):

    def __init__(self):
        self.race = Current_race()

        self.commands = {
            'race' : ['!race'],
            'card' : ['!card', '!board', '!chart']
        }


    def handle_message(self, msg, sender):
        split_msg = msg.lower().split(' ')
        command = split_msg[0]

        if command.startswith('#srl'):
            self.race.set(command, sender)
        elif self.race.race_id != '':
            if command in self.commands['race']:
                self.race.print_info()
            elif command in self.commands['card']:
                self.race.print_card()
        else:
            print("No SRL race set yet!")

    def get_commands(self):
        return flatten(self.commands.values())


class Current_race:

    def __init__(self):

        self.goal = ''
        self.race_id = ''




    def set(self, msg, sender):
        if sender in Settings.EDITORS:
            race_id = msg.replace('#srl-', '')

            self.race_id = race_id

            print(f"The !race command has been updated (#srl-{race_id}).")
            self.print_info()


    def print_info(self):
        self._update()

        url = 'http://www.speedrunslive.com/race/?id='
        entrants = ', '.join([e.get_string() for e in self.entrants])

        str = f"Goal: {self.goal} SRL link: {url} Entrants: {entrants}"
        print(str)

    def print_card(self):
        self._update()

        if self.goal != '':
            if self.goal.startswith('http://www.speedrunslive.com/tools/oot-bingo'):
                print(self.goal)
            else:
                print("Current race not recognized as bingo race. Use !goal to see the goal.")



    def _update(self):
        json = readjson(f"http://api.speedrunslive.com/races/{self.race_id}?callback=renderEntrants")
        if not json:
            print(f"No SRL race found for current race id #srl-{self.race_id}")

        self.goal = json['goal']
        self.entrants = self.get_entrants()


    def get_entrants(self, json):

        entrants = []
        for entrant in json['entrants'].values():
            entrants.append(Entrant(entrant))

        return entrants




class Entrant:

    def __init__(self, json):
        self.name = json['displayname']
        self.trueskill = json['trueskill']
        self.rank = json['rank']
        self.time = json['time']
        self.comment = json['message']

    def get_string(self):
        return f"{self.name} ({self.trueskill})"



