from xwillmarktheBot.Speedrun_stats.Stream_title import get_stream_category
from xwillmarktheBot.Speedrun_stats.SpeedRunsLive.Results.Player_lookup import lookup_SRL_player
from xwillmarktheBot.Abstract_Message_Handler import Message_handler
from xwillmarktheBot.Settings import Settings, Definitions
import logging


class Result_handler(Message_handler):

    def __init__(self, irc_connection):
        super().__init__(irc_connection)
        self.SRL_players = {Settings.STREAMER: lookup_SRL_player(Settings.STREAMER)}
        self.commands = {
            'average': ['!average', '!mean', '!median'],
            'results': ['!results'],
            'pb': ['!pb', '!best'],
            'user_pb': ['!userpb']
        }
        self.race_type = Settings.DEFAULT_RACE_TYPE

    def handle_message(self, msg, sender):
        split_msg = msg.lower().split(' ')
        command = split_msg[0]

        if self.check_valid_arguments(split_msg):

            result_info = Result_info(split_msg, self)
            if command in self.commands['average'] + self.commands['results']:
                self.handle_results(split_msg, result_info)
            else:
                self.handle_pb(result_info)

    def handle_results(self, split_msg, args):
        command = split_msg[0]

        player = args.get_player(self)

        if player:

            result_value = ''

            if command in self.commands['average']:
                result_value, amount = player.get_average(n=args.n, method=command[1:], type=args.type)
            if command in self.commands['results']:
                result_value, amount = player.get_results(n=args.n, type=args.type)

            if (result_value is not None) & (result_value != ''):
                self.send(f"{player.name}'s {command[1:]} for the last {amount} {args.type} races: {result_value}")
            else:
                self.send(f"No recorded {args.type} races found for user {player.name}")

    def handle_pb(self, args):
        logging.debug("Looking up SRL result PB...")

        player = args.get_player(self)
        if player:

            pb = player.get_pb(type=args.type)
            if pb:
                self.send(f"{player.name}'s {args.type} race pb is {pb}.")
            else:
                self.send(f"No recorded {args.type} races found for user {player.name}")

    def get_stream_title_type(self):
        title = get_stream_category()
        matching_types = [type for type in Definitions.RACE_TYPES if type in title]
        if matching_types != []:
            return matching_types[0]

    def get_SRL_player(self, name):
        if name not in self.SRL_players:
            self.send(f"Looking up user {name}...")
            self.SRL_players[name] = lookup_SRL_player(name)

        return self.SRL_players[name]

    def check_valid_arguments(self, split_msg):
        command = split_msg[0]

        if command in self.commands['average'] + self.commands['results']:
            if len(split_msg) > 4:
                return self.send(
                    f'Too many arguments! Please only add a username, integer and/or race type (pick from {Definitions.RACE_TYPES}).')
        else:
            if len(split_msg) > 3:
                return self.send(
                    f'Too many arguments! Please only add a username and/or race type (pick from {Definitions.RACE_TYPES}).')
            if command in self.commands['user_pb']:
                if len(split_msg) < 2:
                    return self.send("Please supply a user!")
        return True


class Result_info:

    def __init__(self, split_msg, result_handler):
        self.n = self.get_n(split_msg)
        self.player_name = None
        for word in split_msg[1:]:
            if (not word.isdigit()) & (not word in Definitions.RACE_TYPES):
                self.player_name = word
        self.type = self.get_type(split_msg, result_handler)

        logging.debug(
            f"Found race arguments. n: {self.n}, player: {self.player_name}, type: {self.type}.")

    def get_player(self, result_handler):

        name = self.player_name
        if not name:
            return result_handler.SRL_players[Settings.STREAMER]
        player = result_handler.get_SRL_player(name)
        if not player:
            return result_handler.send("SRL user not found!")
        else:
            return player


    def get_n(self, split_msg):
        n = 10
        for word in split_msg[1:]:
            if word.isdigit():
                n = int(word)
        return n

    def get_type(self, split_msg, result_handler):
        # look in arguments
        for word in split_msg[1:]:
            if word in Definitions.RACE_TYPES:
                return word
        # look in stream title
        type = result_handler.get_stream_title_type()

        # pick default
        if not type:
            return Settings.DEFAULT_RACE_TYPE
        return type





