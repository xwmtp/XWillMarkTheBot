from Message_handlers.SRC.SRC import *
import Settings
import re

OOT_ID     = "j1l9qz1g"
OOT_EXT_ID = "76rkv4d8"

CONVERT_TERMS = {
    'item manipulation' : 'im',
    'ad' : 'all dungeons',
    'medallions, stones, trials' : 'mst',
    'medallions, stones, barrier' : 'msb',
    'ww' : 'wrong warp',
    'no source requirement' : 'nsr',
    'real time attack' : 'rta',
    'heart piece' : 'hp',
    'nms' : 'no major skips',
    'out of bounds' : 'oob',
    'reverse bottle adventure' : 'rba',
    'rdo' : 'reverse dungeon order',
    'hundo' : '100%',
    'dampe rta' : 'dampe hp rta',
    '37 keys' : '37 water temple keys',
    '37 water keys' : '37 water temple keys',
    'bug limit' : 'unrestricted',
    'glitchless unrestricted' : 'glitchless any% unrestricted'
}

CONVERT_CATS = {
    '100% unrestricted' : '100%',
}

TITLE_BLACKLIST = ['runs', 'run', 'speed', 'short', 'stream', 'playthrough', 'blind']



class Category_matcher:

    def __init__(self):
        self.category_data = {}

    def match_category(self, str):
        print(f'Looking up category {str}...')
        sub_str = self.substitute_abbreviations(CONVERT_TERMS, str)

        # try exact matching
        match = self.find_exact_match(OOT_ID, sub_str)
        if not match:
            match = self.find_exact_match(OOT_EXT_ID, sub_str)

        if match is None:
            logging.info(f"Couldn't find category {str}, searched for {sub_str}.")
            return print(f"Category {sub_str} was not found.")
        else:
            logging.debug(f"Found category match: {match.name}")

        return match

    def match_stream_category(self):
        stream_title = self.get_stream_title()
        title = self.clean_stream_title(stream_title)

        logging.debug(f'Found following stream title: {title}')
        return self.match_category(title)


    def get_stream_title(self):
        return readjson(f"https://decapi.me/twitch/title/{Settings.STREAMER}", text_only=True).lower()


    def clean_stream_title(self, title):
        # remove everything after |
        title = title.split('|', 1)[0]

        # remove everything in () [] brackets
        title = re.sub(r"[\[].*?[\]]", '', title)

        # remove common stream title words
        for term in TITLE_BLACKLIST:
            title = title.replace(term, '')

        # remove any multiple spaces and start/end spaces
        title = ' '.join(title.split())

        return title





    def get_category_data(self, game_id):
        if game_id not in self.category_data.keys():
            self.category_data[game_id] = readjson(f'https://www.speedrun.com/api/v1/games/{game_id}/categories')['data']
        return self.category_data[game_id]


    def find_exact_match(self, category_id, str):
        categories = self.get_category_data(category_id)
        for category in categories:
            name = category['name'].lower()
            category_names = self.get_category_alternatives(name)
            for category_name in category_names:

                if str.startswith(category_name):
                    found_category = Category(category)

                    # add selected subcategory if match can be found
                    remainder = str.replace(category_name + ' ', '')
                    if len(remainder) > 0:
                        for subcategory in found_category.leaderboards.keys():
                            subcat_names = self.get_category_alternatives(subcategory.lower())
                            for subcat in subcat_names:
                                if remainder == subcat.lower():
                                    found_category.selected_subcategory = subcategory

                    return found_category

    def get_category_alternatives(self, category):
        """Returns a list of possible alternative names for a categoryegory (i.e. bug limit for unrestricted)"""

        def delete_brackets(str):
            bracketless = re.sub(r"[\[\(].*?[\]\)]", '', str)
            spaceless = ' '.join(bracketless.split())
            return spaceless

        category_names = set([category])
        category_names.add(delete_brackets(category))
        for name, sub_name in CONVERT_CATS.items():
            new_name = category.replace(name, sub_name)
            category_names.add(new_name)

        if len(category_names) > 1:
            logging.debug(f"Alternatives for categories found: {category_names}")
        return category_names


    def rule_based_match_OOT(self, category_id, str):

        for category in self.get_category_data(category_id):

            name = category['name'].lower()


    def substitute_abbreviations(self, dictionary, str):
        str = str.lower()

        # get rid of possible - surrounded by whitespaces
        str = re.sub(r" *- *", ' ', str)

        for term, sub_term in dictionary.items():
            # only replace if surrounded by non-alfanumeric or string start/end
            str = re.sub(r"(\W|^)" + term + r"(\W|$)", r"\g<1>" + sub_term + r"\g<2>", str)
        return str



