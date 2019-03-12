from xwillmarktheBot.Message_handlers.Speedrun_com.Category_matcher import Category_matcher
from xwillmarktheBot.Message_handlers.Message_handler import Message_handler
from xwillmarktheBot.Message_handlers.Speedrun_com import Stream_title
from xwillmarktheBot.Utils import *
from xwillmarktheBot import Settings


class SRC_handler(Message_handler):

    def __init__(self, irc_connection):
        super().__init__(irc_connection)
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
                return self.send("Please supply a user!")
            user = split_msg[1]
            args = ' '.join(split_msg[2:])
        else:
            user = Settings.STREAMER
            args = msg.replace(f'{command}', '')
            args = args.strip(' ')

        if args == '':
            args = Stream_title.get_stream_category()

        logging.debug('Matching category on stream title...')
        self.send(f'Looking up category {args}...')
        category = self.category_matcher.match_category(args)

        if category is None:
            return self.send(f"Category was not found.")

        # if the selected subcategory remained None, the default will be taken.
        leaderboard = category.get_leaderboard(category.selected_subcategory)

        self.send_wr_pb(command[1:], leaderboard, category, user)


    def send_wr_pb(self, type, leaderboard, category, user):
        space = '' if leaderboard.name == '' else ' - '
        full_category_name = category.name + space + leaderboard.name

        if type == "wr":
            run = leaderboard.get_rank_run()
            if run is None:
                self.send("No world record found for OoT" + full_category_name)
                return
            self.send("The current WR for OoT " + full_category_name + " is " + run.time + " by " + run.player + ".")
        else:
            run = leaderboard.get_user_run(user)
            if run is None:
                self.send("No PB found for OoT " + full_category_name + " by " + user + ".")
                return
            self.send(run.player + "'s PB for OoT " + full_category_name + " is " + run.time + ".")
