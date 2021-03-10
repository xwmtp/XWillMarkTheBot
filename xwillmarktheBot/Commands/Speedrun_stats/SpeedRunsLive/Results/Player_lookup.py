from xwillmarktheBot.Utils import *
from xwillmarktheBot.Commands.Speedrun_stats.SpeedRunsLive.Results.Player import SRL_player
from xwillmarktheBot.Config import Configs


class Player_lookup:

    def __init__(self):
        streamer = Configs.get('streamer')
        self.SRL_players = {streamer: self.find_new_SRL_player(streamer)}

    def get_SRL_player(self, name):
        if name in self.SRL_players.keys():
            reloaded = self.SRL_players[name].reload_data()
            if reloaded:
                return self.SRL_players[name]


        self.SRL_players[name] = self.find_new_SRL_player(name)
        return self.SRL_players[name]


    def find_new_SRL_player(self, user):
        logging.info(f"Looking up user {user}...")

        json = self.get_srl_json(user)

        # user found
        if json:
            return SRL_player(user, json)
        # user not found, try to look up
        else:
            logging.info(f"Trying alternative names for user {user}.")
            return self._try_alt_names(user)

    def get_srl_json(self, user_name):
        srl_url = f"http://api.speedrunslive.com/pastraces?player={user_name}&pageSize=1000"
        return readjson(srl_url)


    def _try_alt_names(self, user):

        alt_names = [user]
        # alternative names found on srl
        alt_names = self._add_src_alt_names(alt_names, user)

        # defined alternative names
        alt_names = self._add_defined_alt_names(alt_names)

        for alt in alt_names:
            srl_json = self.get_srl_json(alt)
            if srl_json:
                return SRL_player(alt, srl_json)


    def _add_defined_alt_names(self, names):
        alt_name_dict = Configs.get_section('alt_names')
        for name, alts in alt_name_dict.items():
            if any([is_lowercase_elem(n, alts) for n in names]):
                if not is_lowercase_elem(name, names):
                    logging.debug(f'Added defined alt name {name}.')
                    names.append(name)
        logging.debug(f'Alternative names (defined): {names}.')
        return names


    def _add_src_alt_names(self, names, user):

        uri_dict = {
            'twitch': 'https://www.twitch.tv/',
            'twitter': 'https://www.twitter.com/',
            'speedrunslive': 'http://www.speedrunslive.com/profiles/#!/'
        }

        logging.debug(f'Known names: {names}')

        json = readjson(f"https://www.speedrun.com/api/v1/users?lookup={user}")
        if json["data"] != []:
            json = json['data'][0]

            # alternative name (possibly different from user)
            logging.debug('looking up name ' + user)
            alt_name = json['names']['international']
            if not is_lowercase_elem(alt_name, names):
                logging.debug(f'Added alt name (international) {alt_name}.')
                names.append(alt_name)

            # social media names
            for platform, uri_start in uri_dict.items():
                if json[platform]:
                    user = json[platform]['uri'].replace(uri_start, '')
                    if not is_lowercase_elem(user, names):
                        logging.debug(f'Added {platform} name {user}.')
                        names.append(user)


        logging.debug(f'Alternative names (src): {names}.')
        return names