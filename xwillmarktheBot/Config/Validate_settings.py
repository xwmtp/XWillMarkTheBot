from xwillmarktheBot.Config import Configs
from xwillmarktheBot.Config import Definitions
from datetime import datetime

def validate_settings():
    # all the required fields have been changed from the default value
    validate_settings_file_edited()

    # message handler settings are all bool
    validate_boolean_settings()

    # string settings are actually strings
    validate_string_settings()

    # SRL race types are valid
    validate_race_types()

    # editors is a list containing the streamer
    validate_editors()

    # default logging level is valid
    validate_logging_level()

    # check if all dates are correct
    validate_dates()

def validate_settings_file_edited():
    default_stream_settings = {
        Configs.get('streamer')  : '123_user_name',
        Configs.get('bot')       : '123_bot__name',
        Configs.get('bot')  : 'oauth:test123'
    }
    for setting, default_value in default_stream_settings.items():
        assert (setting != default_value), "One of the Stream settings in Configs.py has not been filled in! Please fill in your streamer name, bot name, and the bots oauth.\
                                            \nOpen Configs.py (in the root folder xwillmarktheBot/Configs.py) in a text editor and rerun the program afterwards."

def validate_boolean_settings():
    for setting in [Configs.get('speedrun.com'), Configs.get('srl results'), Configs.get('srl races'), Configs.get('print all race entrants')]:
        assert (isinstance(setting, bool)), f"One of the boolean settings ({setting}) in Configs.py is not a bool!"

def validate_string_settings():
    for setting in [Configs.get('streamer'), Configs.get('bot')]:
        assert (isinstance(setting, str)), f"One of the string settings ({setting}) in Configs.py is not a string!"

def validate_race_types():
    race_type_setting = Configs.get('default race type')
    assert (isinstance(race_type_setting, str)), "The default (race) result type in Configs.py is not a string!"
    assert (race_type_setting in Definitions.RACE_TYPES), f"{race_type_setting} in Configs.py is not a valid default (race) result type. Pick one from {Definitions.RACE_TYPES}."

def validate_editors():
    assert (isinstance(Configs.get('editors'), list)), "The EDITORS setting in Configs.py has to be list!"
    assert (Configs.get('streamer') in Configs.get('editors')), "The EDITORS list Configs.py has to contain the STREAMER!"

def validate_logging_level():
    level = Configs.get('console_logging_level')
    assert (level in Definitions.LOGGING_LEVELS), f"The selected console logging level ({level}) in Advanced_settings.py is not a valid logging level! Select on from {Definitions.LOGGING_LEVELS}."

def validate_dates():
    date = Configs.get('latest bingo version date')
    assert (isinstance(date, str)), "The latest bingo version date in Configs.py is not a string!"
    try:
        date = datetime.strptime(date, '%d-%m-%Y')
    except:
        raise ValueError("The latest bingo version date could not be parsed correctly. Please verify that it's in the right format DD-MM-YYYY.")
    assert (date <= datetime.today()), "Please pick a latest bingo version date that is in the past."
