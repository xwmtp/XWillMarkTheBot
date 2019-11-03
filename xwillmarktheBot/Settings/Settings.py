from shutil import copyfile
import configparser
import logging

SETTINGS          = configparser.ConfigParser()
SETTINGS_ADVANCED = configparser.ConfigParser()

def create_settings():
    copyfile(r'xwillmarktheBot/Settings/Templates/Settings.ini', r'Settings.ini')
    copyfile(r'xwillmarktheBot/Settings/Templates/Advanced_settings.ini', r'xwillmarktheBot/Settings/Advanced_settings.ini')


def import_settings():
    global SETTINGS
    SETTINGS.read_file(open('C:/Users/sdste/Dropbox/Programming/xwillmarktheBot/Settings.ini'))
    SETTINGS_ADVANCED.read_file(open('C:/Users/sdste/Dropbox/Programming/xwillmarktheBot/xwillmarktheBot/Settings/Advanced_settings.ini'))

def parse_setting_string(str):
    # parse to list
    if ',' in str:
        logging.debug([s.strip() for s in str.split(',')])
        return [s.strip() for s in str.split(',')]
    # parse to boolean
    if str in ['yes', 'no']:
        return str == 'yes'
    # parse to logging level
    if str in ['debug', 'info', 'warning', 'error']:
        return getattr(logging, str.upper())

    return str

def transform_setting(setting, option):
    if option == 'editors':
        setting = [get('streamer')] + setting
    return setting

def get(option):
    if SETTINGS.sections() == []:
        raise LookupError(f'Attempted to look up setting ({option}) before instantiation.')

    setting = None
    for config in [SETTINGS, SETTINGS_ADVANCED]:
        for section in config.sections():
            if config.has_option(section, option):
                raw_setting = config.get(section, option).lower()
                setting = parse_setting_string(raw_setting)
                setting = transform_setting(setting, option)

    if not setting:
        logging.warning(f"Setting '{option}' does not exist in Settings.ini!")

    return setting

def set(option, value):
    print('todo')