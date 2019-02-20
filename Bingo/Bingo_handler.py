from Bingo.Bingo_player_lookup import get_bingo_player

STREAMER = 'xwillmarktheplace'

class Bingo_handler:

    def __init__(self):
        self.bingo_players = {STREAMER : get_bingo_player(STREAMER)}


    def handle_bingo_message(self, msg):
        split_msg = msg.lower().split(' ')
        command, player, n = self.parse_bingo_message(split_msg)

        if not player:
            return print("SRL user not found!")

        if command in ['average', 'mean', 'median']:
            bingo_value = player.get_average(n=n, method=command)
        if command in ['results']:
            bingo_value = player.get_results(n=n)

        if (bingo_value is not None) & (bingo_value != ''):
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
                    self.bingo_players[user] = get_bingo_player(user)
                player = self.bingo_players[user]

        return command, player, n


