import json
import time
from Utils import *
from Category_matcher import *

STREAMER = 'xwillmarktheplace'


class SRC_handler:

    def __init__(self):
        self.category_matcher = Category_matcher()

    def handle_SRC_message(self, message):
        type = message.split(' ')[0].replace('!', '')
        #TODO: USER PB args
        user = STREAMER
        args = message.replace('!' + type + ' ', '')

        if args == "":
            category = self.category_matcher.match_stream_category()
        else:
            category = self.category_matcher.match_category(args)

        if category is None:
            print("Category " + args + " was not found.")
            return

        # if the selected subcategory remained None, the default will be taken.
        leaderboard = category.get_leaderboard(category.selected_subcategory)
        if type == "wr":
            run = leaderboard.get_rank_run()
            if run is None:
                print("No world record found for OoT" + category.name)
                return
            print("The current world record for OoT " + category.name + " is " + run.time + " by " + run.player + ".")
        else:
            run = leaderboard.get_user_run(user)
            if run is None:
                print("No PB found for " + category.name + " by " + user + ".")
                return
            print(run.player + "'s PB for OoT " + category.name + " is " + run.time + ".")










    def retrieve_stream_title(self, streamer=STREAMER):
        stream_title = readjson("https://decapi.me/twitch/title/" + streamer)







class Category:
    def __init__(self, cat):
        self.id = cat['id']
        self.name = cat['name']
        self.leaderboards = self.import_leaderboards(cat)
        self.selected_subcategory = None # so you can save a subcategory to use later

    def import_leaderboards(self, cat):
        leaderboards = {}
        var_link = self.get_link(cat['links'], 'variables')
        vars_json = readjson(var_link)
        main_leaderboard_url = self.get_link(cat['links'], 'leaderboard')
        if vars_json['data'] == []:
            leaderboards[''] = Leaderboard(main_leaderboard_url)
        else:
            variables = vars_json['data'][0]
            var_id = variables['id']
            for subcat_id, subcat in variables['values']['values'].items():
                subcat_leaderboard_url = main_leaderboard_url + "?var-{var_id}={subcat_id}"
                is_default = subcat_id == variables['values']['default']
                leaderboards[subcat['label']] = Leaderboard(subcat_leaderboard_url, is_default)
        return leaderboards

    def get_link(self, links, name):
        for link in links:
            if link['rel'] == name:
                return link['uri']

    def get_leaderboard(self, category=None):
        for name, leaderboard in self.leaderboards.items():
            if ((category is None) and leaderboard.is_default) or name.lower() == category.lower():
                return leaderboard


class Leaderboard:
    def __init__(self, url, is_default=True):
        self.url = url
        self.is_default = is_default

    def get_rank_run(self, rank=1):
        leaderboard_data = readjson(self.url)
        runs = leaderboard_data['data']['runs']
        if rank > len(runs):
            rank = len(runs)
            print("WARNING: rank higher than amount of submissions. Last place is returned.")
        run = Run(runs[rank - 1])
        assert run.rank == rank
        return run

    def get_user_run(self, user=STREAMER):
        user_id = username_to_id(user)
        if user_id is not None:
            leaderboard_data = readjson(self.url)
            runs = leaderboard_data['data']['runs']
            for entry in runs:
                player = entry['run']['players'][0]
                if 'id' in player.keys() and player['id'] == user_id:
                    return Run(entry)





class Run:

    def __init__(self, entry):
        self.rank = entry['place']
        run = entry['run']
        self.id = run['id']
        self.player = self.get_player(run)
        self.time = self.get_time(run)

    def get_player(self, run_player):
        # pick first player (assume only 1)
        player_url = run_player['players'][0]['uri']
        player_info = readjson(player_url)
        return player_info['data']['names']['international']

    def get_time(self, run):
        seconds = run['times']['primary_t']
        return time.strftime('%H:%M:%S', time.gmtime(seconds))

def username_to_id(name):
    url = "https://www.speedrun.com/api/v1/users?lookup=" + name
    player_info = readjson(url)
    if player_info['data'] != []:
        return player_info['data'][0]['id']



