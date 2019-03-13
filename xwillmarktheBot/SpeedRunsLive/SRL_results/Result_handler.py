from xwillmarktheBot.SpeedRunsLive.SRL_results.SRL_player_lookup import get_SRL_player
from xwillmarktheBot.Abstract_Message_Handler import Message_handler
from xwillmarktheBot import Settings


class Result_handler(Message_handler):

    def __init__(self, irc_connection):
        super().__init__(irc_connection)
        self.SRL_players = {Settings.STREAMER : get_SRL_player(Settings.STREAMER)}
        self.commands = {
            'average' : ['!average', '!mean', '!median'],
            'results' : ['!results']
        }
        self.race_type = Settings.DEFAULT_RESULT_TYPE


    def handle_message(self, msg, sender):
        split_msg = msg.lower().split(' ')
        command, player, n = self.parse_SRL_message(split_msg)

        if not player:
            return self.send("SRL user not found!")

        result_value = ''

        if command in self.commands['average']:
            result_value, amount = player.get_average(n=n, method=command[1:], type = self.race_type)
        if command in self.commands['results']:
            result_value, amount = player.get_results(n=n, type = self.race_type)

        if (result_value is not None) & (result_value != ''):
            self.send(f"{player.name}'s {command[1:]} for the last {amount} {self.race_type} races: {result_value}")
        else:
            self.send(f"No recorded {self.race_type} races found for user {player.name}")


    def parse_SRL_message(self, split_msg):
        # default settings
        n = 15
        player = self.SRL_players[Settings.STREAMER]

        if len(split_msg) > 3:
            raise ValueError('Too many arguments! Please only add a username and integer.')

        command = split_msg[0]

        for word in split_msg[1:]:
            if word.isdigit():
                n = int(word)
            else:
                user = word.lower()
                #todo: convert with alias_dict
                if user not in self.SRL_players:
                    self.send(f"Looking up user {user}...")
                    self.SRL_players[user] = get_SRL_player(user)
                player = self.SRL_players[user]

        return command, player, n


