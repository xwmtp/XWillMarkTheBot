from xwillmarktheBot.SpeedRunsLive.Race import PastRace
from xwillmarktheBot.Utils import *
import datetime


class SRL_player:

    def __init__(self, name, json):
        self.name = name
        self.races = [PastRace(race) for race in json['pastraces']]


        #todo: blacklisting races
        #if self.name.lower() in blacklist_dict.keys():
        #    self.blacklist = blacklist_dict[self.name]



    def get_average(self, n=15, type='bingo', method='average'):
        races = self.select_races(n, type, sort="latest")[:n]

        times = [race.get_entrant(self.name).get_time(seconds=True) for race in races]

        if times == []:
            logging.debug(f'No {type} races found to take average.')
            return None, None

        logging.debug(f'Using method {method}.')
        if method in ['average', 'mean']:
            res = int(mean(times))
        else:
            res = int(median(times))
        return datetime.timedelta(seconds=res), len(races)#.replace(microseconds = 0)

    def get_results(self, n=15, type='bingo', sort='latest'):
        """Return latest or best race results in a comma separated string."""
        result_races = self.select_races(n, type, sort)
        times = [str(race.get_entrant(self.name).get_time()) for race in result_races]
        return ', '.join(times), len(result_races)

    def get_pb(self, type='bingo'):
        race = self.select_races(type=type, sort='best')[0]
        return race.get_entrant(self.name).get_time()


    def select_races(self, n=-1, type='bingo', sort='best', forfeits=False, remove_blacklisted=True):
        if forfeits:
            all_races = self.races
        else:
            all_races = [race for race in self.races if not race.get_entrant(self.name).forfeit]

        selected_races = [race for race in all_races if race.type == type]


        if sort == 'best':
            selected_races = sorted(selected_races, key=lambda r: r.time)
        elif sort == 'latest':
            selected_races = sorted(selected_races, key=lambda r: r.date, reverse=True)

        #todo: blacklist
        #if remove_blacklisted and self.name in blacklist_dict.keys():
        #    races = [race for race in races if str(race.time) not in self.blacklist]

        # Can't select more races than have been found
        if (n > len(selected_races)) or (n == -1):
            n = len(selected_races)
        return selected_races[:n]