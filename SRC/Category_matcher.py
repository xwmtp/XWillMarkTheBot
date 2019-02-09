from Utils import *
from SRC.SRC import *
import re

OOT_ID     = "j1l9qz1g"
OOT_EXT_ID = "76rkv4d8"

CONVERT_TERMS = {
    "item manipulation" : "im",
    "ad" : "all dungeons",
    "medallions, stones, trials" : "mst",
    "medallions, stones, barrier" : "msb",
    "ww" : "wrong warp",
    "no source requirement" : "nsr",
    "real time attack" : "rta",
    "heart piece" : "hp",
    "nms" : "no major skips",
    "out of bounds" : "oob",
    "reverse bottle adventure" : "rba",
    "rdo" : "reverse dungeon order",
    "hundo" : "100%",
    "dampe rta" : "dampe hp rta"
}



class Category_matcher:

    def __init__(self):
        self.category_data = {}

    def match_category(self, str):
        str = self.substitute_abbreviations(CONVERT_TERMS, str)

        # try exact matching
        match = self.find_exact_match(OOT_ID, str)
        if not match:
            match = self.find_exact_match(OOT_EXT_ID, str)

        # None if not found
        return match

    def match_stream_category(self):


        return


    def get_category_data(self, game_id):
        if game_id not in self.category_data.keys():
            self.category_data[game_id] = readjson("https://www.speedrun.com/api/v1/games/" + game_id + "/categories")['data']
        return self.category_data[game_id]


    def find_exact_match(self, category_id, str):
        categories = self.get_category_data(category_id)
        for category in categories:

            name = category['name'].lower()

            if str.startswith(name):
                found_category = Category(category)

                # add selected subcategory if match can be found
                remainder = str.replace(name + ' ', '')
                if len(remainder) > 0:
                    for subcategory in found_category.leaderboards.keys():
                        if remainder == subcategory.lower():
                            found_category.selected_subcategory = subcategory

                return found_category


    def rule_based_match_OOT(self, category_id, str):

        for category in self.get_category_data(category_id):

            name = category['name'].lower()


    def substitute_abbreviations(self, dictionary, str):
        str = str.lower()
        for term, sub_term in CONVERT_TERMS.items():
            # only replace if surrounded by non-alfanumeric or string start/end
            str = re.sub(r"(\W|^)" + term + r"(\W|$)", r"\g<1>" + sub_term + r"\g<2>", str)
        return str



