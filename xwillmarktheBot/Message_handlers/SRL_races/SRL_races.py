from xwillmarktheBot.Utils import *
import datetime

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


    def get_race_link(self):
        return 'http://www.speedrunslive.com/race/?id=' + self.id


    def get_entrants_string(self):
        entrants = sorted(self.entrants, key=lambda x: x.rank)
        entrants_string = ' | '.join([e.get_string() for e in entrants])
        return entrants_string




class Entrant:

    def __init__(self, json):
        self.name = json['displayname']
        self.trueskill = json['trueskill']
        self.rank = json['place']
        self.time = json['time']
        self.comment = json['message']
        self.place = json['place']
        self.status = json['statetext']

    def get_string(self):
        strings = [self.name, f'({self.trueskill})']
        if self.status == 'Finished':
            strings = [f'{str(self.rank)}.'] + strings
            strings.append(f'{self.get_time()}')
        elif self.status == 'Forfeit':
            strings.append('forfeit')

        return ' '.join(strings)

    def get_time(self):
        return datetime.timedelta(seconds=self.time)


# {'id': 'kc1li',
#  'game': {'id': 3977,
#   'name': 'The Legend of Zelda: A Link to the Past Hacks',
#   'abbrev': 'alttphacks',
#   'popularity': 101.0,
#   'popularityrank': 13},
#  'goal': 'SGDE Tournament Race Brogor vs JulienBerlin',
#  'time': 1552050008,
#  'state': 4,
#  'statetext': 'Complete',
#  'filename': '',
#  'numentrants': 2,
#  'entrants': {'Zouizid': {'displayname': 'Zouizid',
#    'place': 1,
#    'time': 6457,
#    'message': '',
#    'statetext': 'Finished',
#    'twitch': 'zouizid',
#    'trueskill': '0'},
#   'julien-berlin': {'displayname': 'julien-berlin',
#    'place': 9998,
#    'time': -1,
#    'message': '',
#    'statetext': 'Forfeit',
#    'twitch': 'julienberlin',
#    'trueskill': '0'}}}
