from Utils import *
from Bingo.Bingo_race import *

class Bingo_player:

    def __init__(self, name, json):
        self.name = name
        self.races = self.extract_races(json)
        self.bingos = [race for race in self.races if race.type == "v92"] #todo: look v92 type shit

        if (self.bingos == []) or (self.bingos is None):
            print(f"No recorded bingo races found for user {name}.")

        #todo: blacklisting races
        #if self.name.lower() in blacklist_dict.keys():
        #    self.blacklist = blacklist_dict[self.name]


    def extract_races(self, json):
        races = []
        for race in json["pastraces"]:
            bingo_race = Bingo_race(race)
            races.append(bingo_race)
        return races



    def get_races(self, n=-1, type = "v92", sort = "best"):

        races = self.select_races(type)

        if n==-1:
            n = len(races)

        if sort == "best":
            sorted_bingos = sorted(races, key=lambda r: r.time)
        elif sort == "latest":
            sorted_bingos = sorted(races, key=lambda r: r.date, reverse=True)
        else:
            sorted_bingos = races
        return sorted_bingos[:n]

    def get_average(self, n=15, type = "v92", avg="average"):
        races = self.select_races(type, sort="latest")[:n]

        times = extract_times(races, seconds=True)
        if times == []:
            return

        if avg == "average" or avg == "mean":
            res = int(mean(times))
        else:
            res = int(median(times))
        return datetime.timedelta(seconds=res)#.replace(microseconds = 0)

    def get_pb(self, type = "v92"):
        race = self.select_races(type)[0]
        return race.time


    def select_races(self, type="v92", sort="best", remove_blacklisted=True):
        if type == "bingo":
            races = self.bingos
        elif type == "v92":
            races = [race for race in self.races if race.type == "v92"]
        elif type == "v93":
            races = [race for race in self.races if race.type == "v93"]
        elif type == "v92+":
            races = [race for race in self.races if ((race.type == "v92") | (race.type == "v93"))]
        else:
            races = self.races

        if sort == "best":
            races = sorted(races, key=lambda r: r.time)
        elif sort == "latest":
            races = sorted(races, key=lambda r: r.date, reverse=True)

        if remove_blacklisted and self.name in blacklist_dict.keys():
            races = [race for race in races if str(race.time) not in self.blacklist]

        return races