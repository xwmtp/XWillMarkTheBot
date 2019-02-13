from SRC.Category_matcher import *

STREAMER='xwillmarktheplace'

class SRC_handler:

    def __init__(self):
        self.category_matcher = Category_matcher()

    def handle_SRC_message(self, msg):
        split_msg = msg.split(' ')
        type = split_msg[0].replace('!', '')
        if type == "userpb":
            if len(split_msg) < 2:
                return print("Please supply a user!")
            user = split_msg[1]
            args = ' '.join(split_msg[2:])
        else:
            user = STREAMER
            args = msg.replace('!' + type + ' ', '')

        if args == "":
            category = self.category_matcher.match_stream_category()
        else:
            category = self.category_matcher.match_category(args)

        if category is None:
            return print("Category " + args + " was not found.")

        # if the selected subcategory remained None, the default will be taken.
        leaderboard = category.get_leaderboard(category.selected_subcategory)

        self.print_wr_pb(type, leaderboard, category, user)


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


    def retrieve_stream_title(self, streamer=STREAMER):
        stream_title = readjson("https://decapi.me/twitch/title/" + streamer)
