import datetime
import isodate

class SRLEntrant:

    def __init__(self, json):
        self.rank = json['place']
        self.time = json['time']
        self.comment = json['message']
        self.place = json['place']

    def get_time(self):
        return datetime.timedelta(seconds=self.time)


class LiveSRLEntrant(SRLEntrant):

    def __init__(self, json):
        super().__init__(json)
        self.name = json['displayname']
        self.trueskill = json['trueskill']
        self.status = json['statetext']
        self.forfeit = self.status.lower() == 'forfeit'

    def get_time(self):
        return datetime.timedelta(seconds=self.time)

    def get_string(self):
        strings = [self.name]
        if self.trueskill:
            strings += f'({self.trueskill})'
        if self.status == 'Finished':
            strings = [f'{str(self.rank)}.'] + strings
            strings.append(f'{self.get_time()}')
        elif self.status == 'Forfeit':
            strings.append('forfeit')
        return ' '.join(strings)


class LiveRacetimeEntrant:

    def __init__(self, json):
        self.name = json['user']['name']
        if json['status']['value'] == 'done':
            self.status = 'Finished'
        elif json['status']['value'] == 'dnf':
            self.status = 'Forfeit'
        else:
            self.status = json['status']['value']
        self.trueskill = None
        self.forfeit = self.status.lower() == 'forfeit'
        self.comment = json['comment']
        self.rank = json['place'] if json['place'] else 999999 # keep entrants that haven't finished at end of list
        self.time = json['finish_time']

    def get_time(self):
        floored_time = self.time.split('.')[0] + 'S'
        return isodate.parse_duration(floored_time)

    def get_string(self):
        strings = [self.name]
        if self.status == 'Finished':
            strings = [f'{str(self.rank)}.'] + strings
            strings.append(f'({self.get_time()})')
        elif self.status == 'Forfeit':
            strings.append('(forfeit)')

        return ' '.join(strings)


class PastEntrant(SRLEntrant):

    def __init__(self, json):
        super().__init__(json)
        self.name = json['player']
        self.forfeit = self.time == -1
