from xwillmarktheBot.Speedrun_stats.SpeedRunsLive.Entrant import LiveSRLEntrant, LiveRacetimeEntrant, PastEntrant
from xwillmarktheBot.Config import Definitions
from datetime import datetime
from abc import ABC, abstractmethod
import logging
import re



class Race(ABC):

    def __init__(self):
        self.entrants = [] # to be overridden in child classes

    def get_entrant(self, name):
        for entrant in self.entrants:
            if entrant.name.lower() == name.lower():
                return entrant


    def determine_type(self, goal, game):
        goal = goal.lower()

        # rando type
        if 'rando' in goal or re.search(r'ootr([^A-Za-z]|$)', goal) or game == 'ootr':
            return 'rando'

        # bingo types
        if ('speedrunslive.com/tools/oot-bingo' in goal or 'ootbingo.github.io/bingo/' in goal) and game == 'oot':
            if 'blackout' in goal:
                return 'blackout'
            if 'short' in goal:
                return 'short-bingo'
            for term in ['long', '3x3', 'anti', 'double', 'bufferless', 'child', 'jp', 'japanese', 'bingo-j']:
                if term in goal:
                    return 'other'

            return 'bingo'

        return 'other'

    def get_entrants_string(self):
        entrants = sorted(self.entrants, key=lambda x: x.rank)
        entrants_string = ' | '.join([e.get_string() for e in entrants])
        return entrants_string


class SRLRace(Race):

    def __init__(self, json):
        super().__init__()
        self.platform = 'srl'
        self.id = json['id']
        self.game = json['game']['abbrev']
        self.goal = json['goal']
        self.type = self.determine_type(self.goal, self.game)
        if self.type not in Definitions.RACE_TYPES:
            logging.error(f'Race got assigned an undefined type ({self.type})!')


    def get_race_link(self):
        return 'http://www.speedrunslive.com/race/?id=' + self.id


class RacetimeRace(Race):
    def __init__(self, json):
        super().__init__()
        self.platform = 'racetime'
        self.id = json['name']
        self.game = json['category']['slug']
        self.goal = f"{json['goal']['name']} {json['info']}"
        self.type = self.determine_type(self.goal, self.game)
        if self.type not in Definitions.RACE_TYPES:
            logging.error(f'Race got assigned an undefined type ({self.type})!')

    def get_race_link(self):
        return f'https://racetime.gg/{self.id}'


class LiveSRLRace(SRLRace):

    def __init__(self, json):
        super().__init__(json)
        self.state = json['statetext']
        self.entrants = [LiveSRLEntrant(e) for e in json['entrants'].values()]


class LiveRacetimeRace(RacetimeRace):

    def __init__(self, json):
        super().__init__(json)
        self.state = json['status']['value']
        self.entrants = [LiveRacetimeEntrant(e) for e in json['entrants']]
        print(self.entrants)


class PastRace(SRLRace):

    def __init__(self, json):
        super().__init__(json)
        self.entrants = [PastEntrant(e) for e in json['results']]
        self.date = int(json['date'])

    def get_date(self):
        return datetime.utcfromtimestamp(int(self.date))

    def get_race_link(self):
        return 'http://www.speedrunslive.com/race/?id=' + self.id