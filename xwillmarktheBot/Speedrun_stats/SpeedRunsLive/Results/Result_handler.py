from xwillmarktheBot.Speedrun_stats.Stream_title import get_stream_category
from xwillmarktheBot.Speedrun_stats.SpeedRunsLive.Results.Player_lookup import Player_lookup
from xwillmarktheBot.Abstract_Message_Handler import Message_handler
from xwillmarktheBot.Config import Configs, Definitions
import logging


class Result_handler(Message_handler):

    def __init__(self):
        super().__init__()
        self.commands = {
            'average': ['!average', '!mean', '!median'],
            'results': ['!results'],
            'pb': ['!pb', '!best'],
            'user_pb': ['!userpb']
        }
        self.player_lookup = Player_lookup()
        self.race_type = Configs.get('default race type')

    def handle_message(self, msg, sender):
        split_msg = msg.lower().split(' ')
        command = split_msg[0]

        argument_error = self.check_valid_arguments(split_msg)
        if argument_error:
            return argument_error

        result_info = Result_info(split_msg, self, sender)
        if command in self.commands['average'] + self.commands['results']:
            return self.handle_results(split_msg, result_info)
        else:
            return self.handle_pb(result_info)

    def handle_results(self, split_msg, args):
        command = split_msg[0]

        player = args.get_player(self)

        if player:

            result_value = ''

            if command in self.commands['average']:
                result_value, amount, forfeits = player.get_average(n=args.n, method=command[1:], type=args.type)
            else: #command in self.commands['results']:
                result_value, amount, forfeits = player.get_results(n=args.n, type=args.type)

            if (result_value is not None) & (result_value != ''):
                return f"{player.name}'s {command[1:]} for the last {amount} {args.type} races: {result_value} (forfeits: {forfeits})"
            else:
                return f"No recorded {args.type} races found for user {player.name}"

        else:
            return "SRL user not found!"

    def handle_pb(self, args):
        logging.debug("Looking up SRL result PB...")

        player = args.get_player(self)
        if player:

            if 'bingo' in args.type and 'all' not in args.type and Configs.get('latest bingo version date') != '':
                disclaimer = ' (for the latest bingo version)'
            else:
                disclaimer = ''


            # for bingo races, only looks at latest version
            pb = player.get_pb(type=args.type)
            if pb:
                return f"{player.name}'s {args.type} race pb{disclaimer} is {pb}."
            else:
                return f"No recorded {args.type} races{disclaimer} found for user {player.name}"
        else:
            "SRL user not found!"

    def get_stream_title_type(self):
        title = get_stream_category()
        matching_types = [type for type in Definitions.RACE_TYPES if type in title]
        if matching_types != []:
            return matching_types[0]

    def check_valid_arguments(self, split_msg):
        command = split_msg[0]

        if command in self.commands['average'] + self.commands['results']:
            if len(split_msg) > 4:
                return f'Too many arguments! Please only add a username, integer and/or race type (pick from {Definitions.RACE_TYPES}).'
        else:
            if len(split_msg) > 3:
                return f'Too many arguments! Please only add a username and/or race type (pick from {Definitions.RACE_TYPES}).'
            if command in self.commands['user_pb']:
                if len(split_msg) < 2:
                    return "Please supply a user!"


class Result_info:

    def __init__(self, split_msg, result_handler, sender):
        self.n = self.get_n(split_msg)
        self.player_name = None
        self.sender = sender
        for word in split_msg[1:]:
            if (not word.isdigit()) & (not word in Definitions.RACE_TYPES):
                self.player_name = word
        self.type = self.get_type(split_msg, result_handler)

        logging.debug(
            f"Found race arguments. n: {self.n}, player: {self.player_name}, type: {self.type}.")

    def get_player(self, result_handler):

        logging.debug('Message sent by: ' + self.sender)
        name = self.player_name
        if not name:
            if Configs.get('respond to user'):
                name = self.sender
            else:
                return result_handler.player_lookup.get_SRL_player(Configs.get('streamer'))
        player = result_handler.player_lookup.get_SRL_player(name)
        if player:
            return player


    def get_n(self, split_msg):
        if split_msg[0] == '!median':
            n = 15
        else:
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
            return Configs.get('default race type')
        return type





