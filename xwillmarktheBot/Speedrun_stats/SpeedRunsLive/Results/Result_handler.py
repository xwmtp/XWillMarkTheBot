from xwillmarktheBot.Speedrun_stats.Stream_title import get_stream_category
from xwillmarktheBot.Speedrun_stats.SpeedRunsLive.Results.Player_lookup import lookup_SRL_player
from xwillmarktheBot.Abstract_Message_Handler import Message_handler
from xwillmarktheBot.Settings import Settings, Definitions
import logging


class Result_handler(Message_handler):

    def __init__(self, irc_connection):
        super().__init__(irc_connection)
        self.SRL_players = {Settings.STREAMER : lookup_SRL_player(Settings.STREAMER)}
        self.commands = {
            'average' : ['!average', '!mean', '!median'],
            'results' : ['!results'],
            'pb'      : ['!pb'],
            'user_pb' : ['!userpb']
        }
        self.race_type = Settings.DEFAULT_RACE_TYPE


    def handle_message(self, msg, sender):
        split_msg = msg.lower().split(' ')
        command = split_msg[0]

        if command in self.commands['average'] + self.commands['results']:
            self.handle_results(split_msg)
        else:
            self.handle_pb(split_msg)


    def handle_results(self, split_msg):
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


    def handle_pb(self, split_msg):
        logging.debug("Looking up SRL result PB")
        command = split_msg[0]

        # pb of specific user
        if command in self.commands['user_pb']:
            if len(split_msg) < 2:
                return self.send("Please supply a user!")
            user = split_msg[1]
            race_type = ' '.join(split_msg[2:])
        # pb of streamer
        else:
            user = Settings.STREAMER
            race_type = ' '.join(split_msg[1:])

        # extract pb from title
        if race_type == '':
            title = get_stream_category()
            matching_types = [type for type in Definitions.RACE_TYPES if type in title]
            if matching_types == []:
                return self.send("No race type found in stream title!")
            else:
                race_type = matching_types[0]

        logging.debug(f"Found race type {race_type}.")

        player = self.get_SRL_player(user)

        if not player:
            return self.send("SRL user not found!")

        pb = player.get_pb(type = race_type)
        if pb:
            self.send(f"{player.name}'s {race_type} race pb is {pb}.")
        else:
            self.send(f"No recorded {race_type} races found for user {player.name}")









    def parse_SRL_message(self, split_msg):
        """Retrieves user and n (amount of race) for !average, !median and !results"""
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
                player = self.get_SRL_player(user)

        return command, player, n


    def get_SRL_player(self, name):
        if name not in self.SRL_players:
            self.send(f"Looking up user {name}...")
            self.SRL_players[name] = lookup_SRL_player(name)

        return self.SRL_players[name]



