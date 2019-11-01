from xwillmarktheBot.Utils import *
from xwillmarktheBot.Speedrun_stats.SpeedRunsLive.Results.Player import SRL_player
from xwillmarktheBot.Settings import Settings



def lookup_SRL_player(user):

    json = _get_srl_json(user)

    # user found
    if json:
        return SRL_player(user, json)
    # user not found, try to look up
    else:
        logging.info(f"Trying alternative names for user {user}.")
        return _try_alt_names(user)


def _get_srl_json(user_name):
    srl_url = f"http://api.speedrunslive.com/pastraces?player={user_name}&pageSize=1000"
    return readjson(srl_url)


def _try_alt_names(user):

    alt_names = [user]
    # alternative names found on srl
    alt_names = _add_src_alt_names(alt_names, user)

    # defined alternative names
    alt_names = _add_defined_alt_names(alt_names)

    for alt in alt_names:
        srl_json = _get_srl_json(alt)
        if srl_json:
            return SRL_player(alt, srl_json)


def _add_defined_alt_names(names):
    for name, alts in Settings.ALT_NAMES.items():
        if any([is_lowercase_elem(n, alts) for n in names]):
            if not is_lowercase_elem(name, names):
                logging.debug(f'Added defined alt name {name}.')
                names.append(name)
    logging.info(f'Alternative names (defined): {names}.')
    return names


def _add_src_alt_names(names, user):

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


    logging.info(f'Alternative names (src): {names}.')
    return names






