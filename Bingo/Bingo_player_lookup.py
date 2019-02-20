from Utils import *
from Bingo.Bingo_player import Bingo_player


def get_bingo_player(user):

    print(f"Looking up user {user}...")
    json = _get_srl_json(user)

    # user found
    if json:
        return Bingo_player(user, json)
    # user not found, try to look up
    else:
        logging.info(f"Trying alternative names for user {user}.")
        return _try_alt_names(user)


def _get_srl_json(user_name):
    srl_url = f"http://api.speedrunslive.com/pastraces?player={user_name}&pageSize=1000"
    return readjson(srl_url)


def _try_alt_names(user):
    json = readjson(f"https://www.speedrun.com/api/v1/users?lookup={user}")

    if json["data"] != []:

        alt_names = _extract_alt_names(json['data'][0], [user])

        for alt in alt_names:
            srl_json = _get_srl_json(alt)
            if srl_json:
                return Bingo_player(alt, srl_json)



def _extract_alt_names(json, known_names=None):

    uri_dict = {
        'twitch': 'https://www.twitch.tv/',
        'twitter': 'https://www.twitter.com/',
        'speedrunslive': 'http://www.speedrunslive.com/profiles/#!/'
    }

    if known_names is None:
        names = []
    else:
        names = known_names.copy()

    logging.debug(f'Known names: {known_names}')

    # alternative name (possibly different fromt user)
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

    names = complement(names, known_names) # delete already known names
    logging.info(f'Alternative names found: {names}.')
    return names






