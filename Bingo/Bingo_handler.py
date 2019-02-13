from Bingo.Bingo_player import *

STREAMER = 'xwillmarktheplace'

class Bingo_handler:

    def __init__(self):
        self.bingo_players = {STREAMER : Bingo_player(STREAMER)}


    def handle_bingo_message(self, msg):
        split_msg = msg.lower().split(' ')
        command, player, n = self.parse_bingo_message(split_msg)

        if command in ['average', 'median']:
            avg = player.get_average(n=n, avg=command[1:])
            bingo_value = avg
        if command in ['results']:
            #todo: bingo types
            result_races = player.get_races(n=n, type='v92', sort='latest')
            times = [str(race.time) for race in result_races]
            bingo_value = ', '.join(times)

        print(f"{player.name}'s {command} for the last {str(n)} bingos: {bingo_value}")



    def parse_bingo_message(self, split_msg):
        # default settings
        n = 15
        player = self.bingo_players[STREAMER]

        if len(split_msg) > 3:
            raise ValueError('Too many arguments! Please only add a username and integer.')

        command = split_msg[0][1:]

        for word in split_msg[1:]:
            if word.isdigit():
                n = int(word)
            else:
                user = word.lower()
                #todo: convert with alias_dict
                if user not in self.bingo_players:
                    self.bingo_players[user] = Bingo_player(user)
                player = self.bingo_players[user]
                #todo: check if player has 'races' attr, otherwise doesn't exist

        return command, player, n

