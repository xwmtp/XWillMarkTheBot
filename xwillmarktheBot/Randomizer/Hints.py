from xwillmarktheBot.Settings import Settings, Definitions
from xwillmarktheBot.Utils import *
import logging
import re

empty_hint_terms = ['location', 'item', 'found_item']
specific_hint_terms = ['30 skulls', '40 skulls', '50 skulls', 'biggoron', 'frogs', 'oot']


def send_current_hints():
    try:
        hints = _read_hint_file()
        hint_dict = _parse_hints(hints)
        return _get_hints(hint_dict)
    except Exception as e:
        logging.critical(f"Error {e} while trying to read hint file, parse hints or get hints.")


def _read_hint_file():
    hints_path = Settings.RANDO_HINTS_DIR / 'rando_hints.txt'

    with open(hints_path) as h:
        hint_lines = h.readlines()

    hints = [l.strip() for l in hint_lines]
    logging.debug('Succesfully read hints file from ' + str(hints_path))
    return hints

def _parse_hints(hints):
    hint_dict = {}

    hint_title = ''
    for hint in hints:
        if not re.match(r'^\d\.', hint):
            # title (way of the hero, barren)
            hint_title = hint
            hint_dict[hint_title] = []
        else:
            # hint
            hint = re.sub(r'^\d\.', '', hint)
            hint_elements = hint.split(';')
            hint_elements = [elem.strip() for elem in hint_elements if elem.strip() not in empty_hint_terms]

            # hint wasn't filled in yet
            if all(elem in empty_hint_terms + specific_hint_terms for elem in hint_elements):
                hint_string = ''
            else:
            # hint is filled in
                hint_string = ' - '.join(hint_elements)

            hint_dict[hint_title].append(hint_string)

    logging.debug('Created hints dictionary: ' + str(hint_dict))
    return hint_dict


def _get_hints(hint_dict):
    to_send = []
    # hints may contain empty strings for default ones that haven't been filled by user
    for title, hints in hint_dict.items():
        clean_hints = [h for h in hints if h != '']
        if len(clean_hints) > 0:
            clean_hints = [f"{i}. {h}" for i, h in enumerate(clean_hints, start=1)]
            to_send.append(f"{title} ({len(clean_hints)}/{len(hints)}): {', '.join(clean_hints)}")
    return to_send



def reset_hints():
    try:
        path = Settings.RANDO_HINTS_DIR
        return copy_file(path, 'rando_hints_template.txt', 'rando_hints.txt')
    except Exception as e:
        logging.critical(f"Error {repr(e)} while trying to read hint file, parse hints or get hints.")
        return False
