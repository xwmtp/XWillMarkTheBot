from Utils import *
from Message_handlers.Bingo.Bingo_race import *

class Bingo_player:

    def __init__(self, name, json):
        self.name = name
        self.races = self.extract_races_from_json(json)
        #todo: look v92 type shit


        #todo: blacklisting races
        #if self.name.lower() in blacklist_dict.keys():
        #    self.blacklist = blacklist_dict[self.name]


    def extract_races_from_json(self, json):
        races = []
        for race in json["pastraces"]:
            bingo_race = Bingo_race(race)
            races.append(bingo_race)
        return races



    def get_average(self, n=15, type = "v92", method="average"):
        races = self.select_races(n, type, sort="latest")[:n]

        times = [race.get_result(self.name).get_time(seconds=True) for race in races]

        if times == []:
            logging.debug('No races found to take average.')
            return

        logging.debug(f'Using method {method}.')
        if method in ['average', 'mean']:
            res = int(mean(times))
        else:
            res = int(median(times))
        return datetime.timedelta(seconds=res)#.replace(microseconds = 0)

    def get_results(self, n=15, type = 'v92', sort='latest'):
        """Return latest or best bingo results in a comma separated string."""
        # todo: bingo types
        result_races = self.select_races(n, type, sort)
        times = [str(race.get_player_time(self.name)) for race in result_races]
        return ', '.join(times)

    def get_pb(self, type = "v92"):
        race = self.select_races(type=type, sort='best')[0]
        return race.get_result(self.name).get_time()


    def select_races(self, n=-1, type="v92", sort="best", forfeits=False, remove_blacklisted=True):
        if forfeits:
            all_races = self.races
        else:
            all_races = [race for race in self.races if not race.get_result(self.name).forfeit]

        if type == "v92":
            races = [race for race in all_races if race.type == "v92"]
        elif type == "v93":
            races = [race for race in all_races if race.type == "v93"]
        elif type == "v92+":
            races = [race for race in all_races if ((race.type == "v92") | (race.type == "v93"))]
        else:
            races = all_races

        if sort == "best":
            races = sorted(races, key=lambda r: r.time)
        elif sort == "latest":
            races = sorted(races, key=lambda r: r.date, reverse=True)

        #todo: blacklist
        #if remove_blacklisted and self.name in blacklist_dict.keys():
        #    races = [race for race in races if str(race.time) not in self.blacklist]

        if (n > len(races)) or (n == -1):
            n = len(races)

        if len(races) == 0:
            print(f'No recorded bingo races found for user {self.name}.')

        return races[:n]