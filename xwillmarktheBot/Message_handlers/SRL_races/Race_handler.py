from xwillmarktheBot.Message_handlers.Message_handler import Message_handler
from xwillmarktheBot.Message_handlers.SRL_races.SRL_races import SRL
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

        self.SRL = SRL()


    def handle_message(self, msg, sender):
        split_msg = msg.lower().split(' ')
        command = split_msg[0]

        self.SRL.update_current_race(Settings.STREAMER)

        if self.SRL.current_race is None:
            return self.send("No SRL race found.")

        # current race
        if command in self.current_race_commands():
            self.send(self.get_current_race_info(command))


    def current_race_commands(self):
        current_race_groups = ['race', 'goal', 'card', 'entrants']
        return flatten([self.commands[group] for group in current_race_groups])



    def get_current_race_info(self, command):
        if (command in self.commands['card']) & (self.SRL.current_race.type != 'bingo'):
            return "Current race is not a bingo. Use !race or !goal."

        answer = ''

        if command in self.commands['goal'] + self.commands['card']:
            answer = self.SRL.current_race.goal

        elif command in self.commands['race']:
            answer = self.SRL.current_race.get_race_link()

        if (command in self.commands['entrants']) | (Settings.PRINT_RACE_ENTRANTS & (command in self.commands['race'])):
            answer = f"{answer} Entrants: {self.SRL.current_race.get_entrants_string()}"

        return answer.strip()




