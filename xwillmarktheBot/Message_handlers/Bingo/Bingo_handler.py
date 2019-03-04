from xwillmarktheBot.Message_handlers.Bingo.Bingo_player_lookup import get_bingo_player
from xwillmarktheBot.Message_handlers.Message_handler import Message_handler
from xwillmarktheBot import Settings


class Bingo_handler(Message_handler):

    def __init__(self, irc_connection):
        super().__init__(irc_connection)
        self.bingo_players = {Settings.STREAMER : get_bingo_player(Settings.STREAMER)}
        self.commands = {
            'average' : ['!average', '!mean', '!median'],
            'results' : ['!results']
        }


    def handle_message(self, msg, sender):
        split_msg = msg.lower().split(' ')
        command, player, n = self.parse_bingo_message(split_msg)

        if not player:
            return self.send("SRL user not found!")

        bingo_value = ''

        if command in self.commands['average']:
            bingo_value, amount = player.get_average(n=n, method=command[1:])
        if command in self.commands['results']:
            bingo_value, amount = player.get_results(n=n)

        if (bingo_value is not None) & (bingo_value != ''):
            self.send(f"{player.name}'s {command[1:]} for the last {amount} bingos: {bingo_value}")
        else:
            self.send(f"No recorded bingo races found for user {player.name}")


    def parse_bingo_message(self, split_msg):
        # default settings
        n = 15
        player = self.bingo_players[Settings.STREAMER]

        if len(split_msg) > 3:
            raise ValueError('Too many arguments! Please only add a username and integer.')

        command = split_msg[0]

        for word in split_msg[1:]:
            if word.isdigit():
                n = int(word)
            else:
                user = word.lower()
                #todo: convert with alias_dict
                if user not in self.bingo_players:
                    self.send(f"Looking up user {user}...")
                    self.bingo_players[user] = get_bingo_player(user)
                player = self.bingo_players[user]

        return command, player, n


