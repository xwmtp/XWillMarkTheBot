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

        if self.check_valid_arguments(split_msg):

            result_info = Result_info(split_msg, self)
            if command in self.commands['average'] + self.commands['results']:
                self.handle_results(split_msg, result_info)
            else:
                self.handle_pb(split_msg, result_info)


    def handle_results(self, split_msg, args):
        command = split_msg[0]

        if not args.player:
            return self.send("SRL user not found!")

        result_value = ''

        if command in self.commands['average']:
            result_value, amount = args.player.get_average(n=args.n, method=command[1:], type = args.type)
        if command in self.commands['results']:
            result_value, amount = args.player.get_results(n=args.n, type = args.type)

        if (result_value is not None) & (result_value != ''):
            self.send(f"{args.player.name}'s {command[1:]} for the last {amount} {args.type} races: {result_value}")
        else:
            self.send(f"No recorded {args.type} races found for user {args.player.name}")


    def handle_pb(self, split_msg, args):
        logging.debug("Looking up SRL result PB...")

        if args.player:

            pb = args.player.get_pb(type = args.type)
            if pb:
                self.send(f"{args.player.name}'s {args.type} race pb is {pb}.")
            else:
                self.send(f"No recorded {args.type} races found for user {args.player.name}")



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
        self.n = 15
        self.player = None
        self.type = Settings.DEFAULT_RACE_TYPE

        self.parse_SRL_message(split_msg, result_handler)
        logging.debug(f"Found race arguments. n: {self.n}, player: {self.player.name if self.player is not None else None}, type: {self.type}.")

    def parse_SRL_message(self, split_msg, result_handler):
        """Overwrites default result arguments with info found in message"""
        for word in split_msg[1:]:
            if word.isdigit():
                self.n = int(word)
            elif word in Definitions.RACE_TYPES:
                self.type = word
            else:
                user = word
                # todo: convert with alias_dict
                self.player = result_handler.get_SRL_player(user)

        if not self.player:
            if (split_msg[0] in result_handler.commands['user_pb']):
                result_handler.send("SRL user not found!")
            else:
                self.player = result_handler.SRL_players[Settings.STREAMER]


