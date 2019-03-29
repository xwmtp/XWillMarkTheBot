from xwillmarktheBot.Speedrun_stats.SpeedRunsLive.Race import PastRace
from xwillmarktheBot.Settings import Definitions, Settings
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
        races = self.select_races(type=type, sort='best')
        if races != []:
            return races[0].get_entrant(self.name).get_time()


    def select_races(self, n=-1, type='bingo', sort='best', forfeits=False, remove_blacklisted=True):
        if type not in Definitions.RACE_TYPES:
            return []
        race_type = str.replace(type, 'all-', '')

        if forfeits:
            all_races = self.races
        else:
            all_races = [race for race in self.races if not race.get_entrant(self.name).forfeit]

        if type == 'srl':
            selected_races = all_races
        else:
            selected_races = [race for race in all_races if race.type == race_type]

        selected_races = self.select_dates(selected_races, type)


        if sort == 'best':
            selected_races = sorted(selected_races, key=lambda r: r.get_entrant(self.name).get_time())
        elif sort == 'latest':
            selected_races = sorted(selected_races, key=lambda r: r.date, reverse=True)

        #todo: blacklist
        #if remove_blacklisted and self.name in blacklist_dict.keys():
        #    races = [race for race in races if str(race.time) not in self.blacklist]

        # Can't select more races than have been found
        if (n > len(selected_races)) or (n == -1):
            n = len(selected_races)
        return selected_races[:n]

    def select_dates(self, races, type):

        if ('bingo' in type) & ('all' not in type):
            if Settings.LATEST_BINGO_VERSION_DATE != '':
                version_date = datetime.datetime.strptime(Settings.LATEST_BINGO_VERSION_DATE, '%d-%m-%Y')

                races = [race for race in races if race.get_date() >= version_date]

        return races

