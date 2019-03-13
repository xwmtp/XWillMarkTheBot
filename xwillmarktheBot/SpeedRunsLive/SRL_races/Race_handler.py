from xwillmarktheBot.Abstract_Message_Handler import Message_handler
from xwillmarktheBot.SpeedRunsLive.Race import LiveRace
from xwillmarktheBot import Settings
from xwillmarktheBot.Utils import *

class Race_handler(Message_handler):

    def __init__(self, irc_connection):

        super().__init__(irc_connection)

        self.commands = {
            'race' : ['!race'],
            'card' : ['!card', '!board', '!chart'],
            'goal' : ['!goal'],
            'entrants' : ['!entrants']
        }

        self.live_race = None


    def handle_message(self, msg, sender):
        split_msg = msg.lower().split(' ')
        command = split_msg[0]

        self.update_live_race(Settings.STREAMER)

        if self.live_race is None:
            return self.send("No SRL race found.")

        def live_race_commands(self):
            live_race_groups = ['race', 'goal', 'card', 'entrants']
            return flatten([self.commands[group] for group in live_race_groups])

        # current race
        if command in live_race_commands():
            self.send(self.get_live_race_info(command))



    def update_live_race(self, player):

        def is_entrant(player, race):
            entrants = race['entrants'].keys()
            return player.lower() in [e.lower() for e in entrants]

        json = readjson('http://api.speedrunslive.com/races')
        for race in json['races']:
            if is_entrant(player, race):
                self.live_race = LiveRace(race)
                # if the race isn't finished, stop looking
                if self.live_race.state != 'Complete':
                    return



    def get_live_race_info(self, command):
        if (command in self.commands['card']) & (self.SRL.live_race.type != 'bingo'):
            return "Current race is not a bingo. Use !race or !goal."

        answer = ''

        if command in self.commands['goal'] + self.commands['card']:
            answer = self.live_race.goal

        elif command in self.commands['race']:
            answer = self.live_race.get_race_link()

        if (command in self.commands['entrants']) | (Settings.PRINT_RACE_ENTRANTS & (command in self.commands['race'])):
            answer = f"{answer} Entrants: {self.live_race.get_entrants_string()}"

        return answer.strip()




