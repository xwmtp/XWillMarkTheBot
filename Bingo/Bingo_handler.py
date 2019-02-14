from Bingo.Bingo_player import *

STREAMER = 'xwillmarktheplace'

class Bingo_handler:

    def __init__(self):
        self.bingo_players = {STREAMER : self.get_bingo_player(STREAMER)}


    def handle_bingo_message(self, msg):
        split_msg = msg.lower().split(' ')
        command, player, n = self.parse_bingo_message(split_msg)

        if not player:
            return print("User not found!")

        if command in ['average', 'mean', 'median']:
            avg = player.get_average(n=n, method=command)
            bingo_value = avg
        if command in ['results']:
            #todo: bingo types
            result_races = player.select_races(n=n, type='v92', sort='latest')
            times = [str(race.get_player_time(player.name)) for race in result_races]
            bingo_value = ', '.join(times)

        print(f"{player.name}'s {command} for the last {str(n)} bingos: {bingo_value}")



    def parse_bingo_message(self, split_msg):
        # default settings
        n = 15
        player = self.bingo_players[STREAMER]

        if len(split_msg) > 3:
            print(split_msg) #t
            raise ValueError('Too many arguments! Please only add a username and integer.')

        command = split_msg[0][1:]

        for word in split_msg[1:]:
            if word.isdigit():
                n = int(word)
            else:
                user = word.lower()
                #todo: convert with alias_dict
                if user not in self.bingo_players:
                    self.bingo_players[user] = self.get_bingo_player(user)
                player = self.bingo_players[user]

        return command, player, n


    def get_bingo_player(self, user):

        json = readjson(f"http://api.speedrunslive.com/pastraces?player={user}&pageSize=1000")
        # user not found
        if not json:
            userURL = f"https://www.speedrun.com/api/v1/users?lookup={user}"
            userData = readjson(userURL)
            if userData["data"] != []:
                name = userData['data'][0]['names']['international']
                self.get_bingo_player(name)
        else:
            return Bingo_player(user, json)

