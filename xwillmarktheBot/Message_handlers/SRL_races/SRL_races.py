from xwillmarktheBot.Utils import *

class SRL():


    def __init__(self):
        self.current_race = None

    def update_current_race(self, player):

        def is_entrant(player, race):
            entrants = race['entrants'].keys()
            return player.lower() in [e.lower() for e in entrants]

        json = readjson('http://api.speedrunslive.com/races')
        for race in json['races']:
            if is_entrant(player, race):
                self.current_race = Race(race)
                # if the race isn't finished, stop looking
                if self.current_race.state != 'Complete':
                    return


class Race:

    def __init__(self, json):
        self.id = json['id']
        self.game = json['game']['name']
        self.goal = json['goal']
        self.state = json['statetext']
        self.entrants = self.get_entrants(json)
        self.type = self.determine_type(self.goal)


    def get_entrants(self, json):
        return [Entrant(e) for e in json['entrants'].values()]

    def determine_type(self, goal):
        for type in ['bingo', 'rando']:
            if type in goal:
                return type
        else:
            return 'other'

    def get_entrants_string(self):
        entrants_string = ', '.join([e.get_string() for e in self.entrants])
        return entrants_string

    def get_race_link(self):
        return 'http://www.speedrunslive.com/race/?id=' + self.id





class Entrant:

    def __init__(self, json):
        self.name = json['displayname']
        self.trueskill = json['trueskill']
        self.rank = json['place']
        self.time = json['time']
        self.comment = json['message']

    def get_string(self):
        return f"{self.name} ({self.trueskill})"