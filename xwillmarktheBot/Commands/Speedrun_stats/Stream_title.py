from xwillmarktheBot.Utils import *
from xwillmarktheBot.Config import Configs
import re

TITLE_BLACKLIST = ['runs', 'run', 'speed', 'short', 'stream', 'playthrough', 'blind']

def get_stream_category():
    title = readjson(f"https://decapi.me/twitch/title/{Configs.get('streamer')}", text_only=True).lower()
    return clean_stream_title(title)

def clean_stream_title(title):
    # remove everything after |
    title = title.split('|', 1)[0]

    # remove everything in () [] brackets
    title = re.sub(r"[\[].*?[\]]", '', title)

    # remove everthing following a !
    title = re.sub(r"!\S+", '', title)

    # remove common stream title words
    for term in TITLE_BLACKLIST:
        title = title.replace(term, '')

    # remove any multiple spaces and start/end spaces
    title = ' '.join(title.split())

    return title
