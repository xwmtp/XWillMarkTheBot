import datetime

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