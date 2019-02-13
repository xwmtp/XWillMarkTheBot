from Utils import *

class Bingo_player:

    def __init__(self, name, from_file=False):
        self.name = name

        #try:
        self.json = readjson("http://api.speedrunslive.com/pastraces?player=" + name + "&pageSize=1000")
        if not self.json:
            userURL = "https://www.speedrun.com/api/v1/users?lookup=" + name
            userData = readjson(userURL)
            if userData["data"] == []:
                print("User not found.")
            else:
                name = userData['data'][0]['names']['international']
                self.__init__(name, from_file)
                return
        results = []
        for race in self.json["pastraces"]:
            tuple = retrieve_race_info(race, name, rest=True)
            if tuple != None:
                (date, time, goal, comment) = tuple
                results.append(Race(date, time, goal, comment, name))
        self.races = results
        self.bingos = [race for race in self.races if race.type == "v92"]
        if (self.bingos == []) or (self.bingos is None):
            print("No recorded bingo races found for user {}.".format(self.name))

        if self.name.lower() in blacklist_dict.keys():
            self.blacklist = blacklist_dict[self.name]

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