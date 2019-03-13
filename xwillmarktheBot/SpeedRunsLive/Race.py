from xwillmarktheBot.SpeedRunsLive.Entrant import LiveEntrant, PastEntrant

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