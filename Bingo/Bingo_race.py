import datetime
import re

class Bingo_race:

    def __init__(self, race):
        self.date = int(race['date']) #todo: convert from timestamp?
        self.goal = race['goal']
        self.json = race
        self.type = self.extract_type()
        self.seed = self.extract_seed()
        self.entrants = {}

    def get_result(self, user):
        if user in self.entrants:
            return self.entrants[user]

        for entrant in self.json['results']:
            time = entrant['time']
            if (entrant['player'] == user.lower()) & (time != -1):
                bingo_result = Bingo_result(entrant)
                self.entrants[user] = bingo_result
                return bingo_result

    def get_player_time(self, user):
        race_result = self.get_result(user)
        return race_result.get_time()
            
            
    def extract_type(self):
        url = self.goal.lower()

        type_dict ={
            'http://www.speedrunslive.com/tools/oot-bingo?mode=normal' : 'v92',
            'http://www.buzzplugg.com/bryan/v9.2NoSaria/' : 'NoSaria',
            'series' : 'ocs',
            'championship' : 'ocs'
        }

        for name in ['blackout', 'v4', 'v5', 'v6', 'v7', 'v8', 'v9.1']:
            if name in url:
                return name.replace('.', '')

        for pattern, type in type_dict.items():
            if pattern in url:
                return type

        return 'other'

    def extract_seed(self):
        url = self.goal.lower()
        seed = re.search(r"seed=(\d)+", url)
        if seed:
            seed = seed.group()
        else:
            seed = "-----"
        digit = seed.replace("seed=", "")
        return digit


    def isBingo(self):
        return "bingo" in self.url






class Bingo_result:

    def __init__(self, entrant):
        self.name = entrant['player']
        self.time = datetime.timedelta(seconds=entrant['time'])
        self.comment = entrant['message']
        self.row = self.extract_row(self.comment)


    def extract_row(self, comment):
        str = "((((r(ow)?)|(c(ol)?))( )?(\d))|(tl(-| )?br)|(bl(-| )?tr))"

        match = re.search(str, comment, re.IGNORECASE)
        if match:
            return match.group().lower()
        else:
            return "BLANK"

    def get_time(self, seconds=True):
        if seconds:
            return self.time.total_seconds()
        else:
            return self.time





    #todo is this function needed?
    #
    # def print_race(self, url = False):
    #     print_list = [str(self.date), str(self.time), self.type, self.seed, self.row, self.comment,]
    #     if url:
    #         print_list.append(self.url)
    #     print("\t".join(print_list))