from xwillmarktheBot.Speedrun_stats.SpeedRunsLive.Race import PastRace
from xwillmarktheBot.Settings import Definitions, Settings
from xwillmarktheBot.Utils import *
import datetime


class SRL_player:

    def __init__(self, name, json):
        logging.info(f'Creating player {name}')
        self.name = name
        self.races = [PastRace(race) for race in json['pastraces']]
        self.typeof = type

        #todo: blacklisting races


    def reload_data(self):
        logging.info(f'Reloading data of player {self.name}')

        updated_json = readjson(f"http://api.speedrunslive.com/pastraces?player={self.name}&pageSize=1000")
        if updated_json:
           self.races = [PastRace(race) for race in updated_json['pastraces']]
           return True
        else:
            logging.info(f'Reloading data of player {self.name} failed')
            return False


    def get_average(self, n=15, type='bingo', method='average'):
        races = self.select_races(n, type, sort="latest", latest_version=False)[:n]

        times = [race.get_entrant(self.name).get_time(seconds=True) for race in races]

        if times == []:
            logging.debug(f'No {type} races found to take average.')
            return None, None, None

        forfeits = self.get_forfeit_count(n, type, races)


        logging.debug(f'Using method {method}.')
        if method in ['average', 'mean']:
            res = int(mean(times))
        else:
            res = int(median(times))
        return datetime.timedelta(seconds=res), len(races), forfeits


    def get_results(self, n=15, type='bingo', sort='latest'):
        """Return latest or best race results in a comma separated string."""
        result_races = self.select_races(n, type, sort, latest_version=False)
        times = [str(race.get_entrant(self.name).get_time()) for race in result_races]
        forfeits = self.get_forfeit_count(n, type, result_races)

        return ', '.join(times), len(result_races), forfeits

    def get_forfeit_count(self, n, type, races):
        """Get the amount of forfeits in a list of races that happened in the last 5. Assumes races is sorted by latest date."""
        oldest_race = races[-1]
        logging.debug(f'Race nr {n}: {oldest_race.date}, {oldest_race.get_entrant(self.name).get_time()}')
        all_races = self.select_races(-1, type, sort='latest', forfeits=True, latest_version=False)
        forfeit_races = [race for race in all_races if
                         race.date > oldest_race.date and race.get_entrant(self.name).forfeit]
        return len(forfeit_races)


    def get_pb(self, type='bingo'):
        races = self.select_races(type=type, sort='best', latest_version=True)
        if races != []:
            return races[0].get_entrant(self.name).get_time()


    def select_races(self, n=-1, type='bingo', sort='best', forfeits=False, latest_version=True, remove_blacklisted=True):
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

        # only look at the latest bingo version
        if latest_version:
            selected_races = self.select_dates(selected_races, type)


        if sort == 'best':
            selected_races = sorted(selected_races, key=lambda r: r.get_entrant(self.name).get_time())
        elif sort == 'latest':
            selected_races = sorted(selected_races, key=lambda r: r.date, reverse=True)

        #todo: blacklist

        if (n > len(selected_races)) or (n == -1):
            n = len(selected_races)
        return selected_races[:n]


    def select_dates(self, races, type):
        if ('bingo' in type) & ('all' not in type):
            if Settings.LATEST_BINGO_VERSION_DATE != '':
                version_date = datetime.datetime.strptime(Settings.LATEST_BINGO_VERSION_DATE, '%d-%m-%Y')

                races = [race for race in races if race.get_date() >= version_date]

        return races


