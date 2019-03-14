from xwillmarktheBot.Settings import Settings, Definitions
import re

default_hint_terms = ['location', 'item', 'found_item']


def send_current_hints():
    hints = _read_hint_file()
    hint_dict = _parse_hints(hints)
    _send_hints(hint_dict)


def _read_hint_file():
    hints_path = Definitions.ROOT_DIR / 'RandoHints/rando_hints.txt'

    with open(hints_path) as h:
        hint_lines = h.readlines()

    return [l.strip() for l in hint_lines]

def _parse_hints(hints):
    hint_dict = {}

    hint_title = ''
    for hint in hints:
        if not re.match(r'^\d\.', hint):
            # hint is actually a title
            hint_title = hint
            hint_dict[hint_title] = []
            print(hint_title)
        else:
            hint = re.sub(r'^\d\.', '', hint)
            hint = re.sub(r'.+:', '', hint)
            hint_elements = hint.split(';')
            hint_elements = [elem.strip() for elem in hint_elements if elem.strip() not in default_hint_terms]

            if not all(elem in default_hint_terms for elem in hint_elements):
                hint_string = ' - '.join(hint_elements)
                hint_dict[hint_title].append(hint_string)
                print(hint_string)
    return hint_dict

def _send_hints(hint_dict):
    for title, hint in hint_dict.items()
        x=4



def reset_hints():
    x=5