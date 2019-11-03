from xwillmarktheBot.Settings import Settings
from xwillmarktheBot.Settings import Definitions
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

    # editors is a list contraining the streamer
    validate_editors()

    # default logging level is valid
    validate_logging_level()

    # check if all dates are correct
    validate_dates()

def validate_settings_file_edited():
    default_stream_settings = {
        Settings.get('streamer')  : '123_user_name',
        Settings.get('bot')       : '123_bot__name',
        Settings.get('bot')  : 'oauth:test123'
    }
    for setting, default_value in default_stream_settings.items():
        assert (setting != default_value), "One of the Stream settings in Settings.py has not been filled in! Please fill in your streamer name, bot name, and the bots oauth.\
                                            \nOpen Settings.py (in the root folder xwillmarktheBot/Settings.py) in a text editor and rerun the program afterwards."

def validate_boolean_settings():
    for setting in [Settings.get('speedrun.com'), Settings.get('srl results'), Settings.get('srl races'), Settings.get('print all race entrants')]:
        assert (isinstance(setting, bool)), f"One of the boolean settings ({setting}) in Settings.py is not a bool!"

def validate_string_settings():
    for setting in [Settings.get('streamer'), Settings.get('bot')]:
        assert (isinstance(setting, str)), f"One of the string settings ({setting}) in Settings.py is not a string!"

def validate_race_types():
    race_type_setting = Settings.get('default race type')
    assert (isinstance(race_type_setting, str)), "The default (race) result type in Settings.py is not a string!"
    assert (race_type_setting in Definitions.RACE_TYPES), f"{race_type_setting} in Settings.py is not a valid default (race) result type. Pick one from {Definitions.RACE_TYPES}."

def validate_editors():
    assert (isinstance(Settings.get('editors'), list)), "The EDITORS setting in Settings.py has to be list!"
    assert (Settings.get('streamer') in Settings.get('editors')), "The EDITORS list Settings.py has to contain the STREAMER!"

def validate_logging_level():
    level = Settings.get('CONSOLE_LOGGING_LEVEL')
    assert (level in Definitions.LOGGING_LEVELS), f"The selected console logging level ({level}) in Advanced_settings.py is not a valid logging level! Select on from {Definitions.LOGGING_LEVELS}."

def validate_dates():
    date = Settings.get('latest bingo version date')
    assert (isinstance(date, str)), "The latest bingo version date in Settings.py is not a string!"
    try:
        date = datetime.strptime(date, '%d-%m-%Y')
    except:
        raise ValueError("The latest bingo version date could not be parsed correctly. Please verify that it's in the right format DD-MM-YYYY.")
    assert (date <= datetime.today()), "Please pick a latest bingo version date that is in the past."