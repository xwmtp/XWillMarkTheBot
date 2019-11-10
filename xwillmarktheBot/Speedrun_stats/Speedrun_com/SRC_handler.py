from xwillmarktheBot.Speedrun_stats.Speedrun_com.Category_matcher import Category_matcher
from xwillmarktheBot.Abstract_Message_Handler import Message_handler
from xwillmarktheBot.Speedrun_stats import Stream_title
from xwillmarktheBot.Settings import Configs


class SRC_handler(Message_handler):

    def __init__(self):
        super().__init__()
        self.category_matcher = Category_matcher()
        self.commands = {
            'user_lookup' : ['!userpb'],
            'default'     : ['!pb', '!wr'],
            'leaderboard' : ['!leaderboard', '!leaderboards', '!src']
        }

    def handle_message(self, msg, sender):
        split_msg = msg.split(' ')
        command = split_msg[0]

        # pb of specific user
        if command in self.commands['user_lookup']:
            if len(split_msg) < 2:
                return "Please supply a user!"
            user = split_msg[1]
            args = ' '.join(split_msg[2:])
        else:
        # pb of streamer
            if Configs.get('respond to user'):
                user = sender
            else:
                user = Configs.get('streamer')
            args = msg.replace(f'{command}', '').strip(' ')

        # extract pb from title
        if args == '':
            from_title = True
            args = Stream_title.get_stream_category()
        else:
            from_title = False

        category = self.category_matcher.match_category(args)

        if category is None:
            str = ' Try adding a category as an argument (i.e. !pb no im/ww).' if from_title else ''
            return 'Category not found.' + str

        if command in self.commands['leaderboard']:
            return category.weblink
        else:
            # if the selected subcategory remained None, the default will be taken.
            leaderboard = category.get_leaderboard(category.selected_subcategory)


            return self.wr_pb(command[1:], leaderboard, category, user)


    def wr_pb(self, type, leaderboard, category, user):
        space = '' if leaderboard.name == '' else ' - '
        full_category_name = category.name + space + leaderboard.name

        if type == "wr":
            run = leaderboard.get_rank_run()
            if run is None:
                return "No world record found for OoT" + full_category_name
            return "The current WR for OoT " + full_category_name + " is " + run.time + " by " + run.player + "."
        else:
            run = leaderboard.get_user_run(user)
            if run is None:
                return "No PB found for OoT " + full_category_name + " by " + user + "."
            return run.player + "'s PB for OoT " + full_category_name + " is " + run.time + "."
