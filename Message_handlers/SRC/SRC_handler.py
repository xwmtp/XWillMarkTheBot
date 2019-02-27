from Message_handlers.SRC.Category_matcher import Category_matcher
from Message_handlers.Message_handler import Message_handler
from Utils import *
import Settings

class SRC_handler(Message_handler):

    def __init__(self):
        self.category_matcher = Category_matcher()
        self.commands = {
            'user_lookup' : ['!userpb'],
            'default'     : ['!pb', '!wr']
        }

    def handle_message(self, msg, sender):
        split_msg = msg.split(' ')
        command = split_msg[0]

        if command in self.commands['user_lookup']:
            if len(split_msg) < 2:
                return print("Please supply a user!")
            user = split_msg[1]
            args = ' '.join(split_msg[2:])
        else:
            user = Settings.STREAMER
            args = msg.replace(f'{command}', '')
            args = args.strip(' ')

        if args == '':
            logging.debug('Matching category on stream title...')
            category = self.category_matcher.match_stream_category()
        else:
            category = self.category_matcher.match_category(args)

        if category is not None:
            # if the selected subcategory remained None, the default will be taken.
            leaderboard = category.get_leaderboard(category.selected_subcategory)

            self.print_wr_pb(command[1:], leaderboard, category, user)


    def print_wr_pb(self, type, leaderboard, category, user):
        space = '' if leaderboard.name == '' else ' - '
        full_category_name = category.name + space + leaderboard.name

        if type == "wr":
            run = leaderboard.get_rank_run()
            if run is None:
                print("No world record found for OoT" + full_category_name)
                return
            print(
                "The current WR for OoT " + full_category_name + " is " + run.time + " by " + run.player + ".")
        else:
            run = leaderboard.get_user_run(user)
            if run is None:
                print("No PB found for OoT " + full_category_name + " by " + user + ".")
                return
            print(run.player + "'s PB for OoT " + full_category_name + " is " + run.time + ".")


    def retrieve_stream_title(self, streamer=Settings.STREAMER):
        stream_title = readjson("https://decapi.me/twitch/title/" + streamer)
