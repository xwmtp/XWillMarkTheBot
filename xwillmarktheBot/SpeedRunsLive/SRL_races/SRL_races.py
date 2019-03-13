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
        self.type = self.determine_type(self.goal)
        self.entrants = [] # to be defined in child classes

    def get_entrant(self, name):
        for entrant in self.entrants:
            if entrant.name.lower() == name.lower():
                return entrant


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



class LiveRace(Race):

    def __init__(self, json):
        super().__init__(json)
        self.state = json['statetext']
        self.entrants = [LiveEntrant(e) for e in json['entrants'].values()]


class PastRace(Race):

    def __init__(self, json):
        super().__init__(json)
        self.entrants = [PastEntrant(e) for e in json['results']]
        self.date = int(json['date'])








class Entrant:

    def __init__(self, json):
        self.rank = json['place']
        self.time = json['time']
        self.comment = json['message']
        self.place = json['place']


    def get_time(self, seconds=False):
        if seconds:
            return self.time
        else:
            return datetime.timedelta(seconds=self.time)


class LiveEntrant(Entrant):

    def __init__(self, json):
        super().__init__(json)

        self.name = json['displayname']
        self.status = json['statetext']
        self.trueskill = json['trueskill']
        self.forfeit = self.status.lower() == 'Forfeit'


    def get_string(self):
        strings = [self.name, f'({self.trueskill})']

        if self.status == 'Finished':
            strings = [f'{str(self.rank)}.'] + strings
            strings.append(f'{self.get_time()}')

        elif self.status == 'Forfeit':
            strings.append('forfeit')

        return ' '.join(strings)



class PastEntrant(Entrant):

    def __init__(self, json):
        super().__init__(json)

        self.name = json['player']
        self.forfeit = self.time == -1

