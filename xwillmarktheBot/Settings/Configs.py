from xwillmarktheBot.Settings import Definitions
from shutil import copyfile
import configparser
import logging
import sys


class Config:

    def __init__(self, name, file_location):
        self.name = name
        self.config_parser = configparser.ConfigParser()
        self.file_location = file_location

    def load_settings(self):
        self.config_parser.read_file(open(f'{self.file_location}//{self.name}.ini'))
        self.dict = {s:dict(self.config_parser.items(s)) for s in self.config_parser.sections()}
        self.dict = self.parse_dict_values(self.dict)
        if self.dict == {}:
            raise ValueError(f'Empty config dictionary, no setting were found.')

    def copy_from_template(self):
        base_name = self.name.split('-')[0]
        copyfile(rf'xwillmarktheBot/Settings/Templates/{base_name}.ini', f'{self.file_location}/{self.name}.ini')


    def parse_dict_values(self, dct):

        def parse_setting_string(str):
            str = str.lower()
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
                if not isinstance(setting, list):
                    setting = [setting]
                setting = [get('streamer')] + setting
            if option == 'racetime games' and not isinstance(setting, list):
                return [setting]

            return setting

        for section, settings in dct.items():
            for option, value in settings.items():
                parsed_setting = parse_setting_string(value)
                transformed_setting = transform_setting(parsed_setting, option)
                dct[section][option] = transformed_setting
        return dct






if len(sys.argv) < 2:
    raise ValueError('No OAUTH or Discord token provided, please provide it as a sys arg.\
                      \nPlease read the manual at https://github.com/xwmtp/xwillmarktheBot/blob/master/README.md for more information.' )
else:
    token = sys.argv[1]

if token.startswith('oauth:'):
    connection_type = 'twitch'
else:
    connection_type = 'discord'

configs = [
    Config(f'Settings-{connection_type}', Definitions.ROOT_DIR),
    Config(f'Settings_advanced-{connection_type}', Definitions.ROOT_DIR / 'xwillmarktheBot/Settings')
]


def create_settings():
    for config in configs:
        config.copy_from_template()

def import_settings():
    for config in configs:
        config.load_settings()



def get(option):
    option = option.lower()
    for config in configs:
        for section in config.dict.keys():
            if option in config.dict[section].keys():
                return config.dict[section][option]

    logging.warning(f"Setting '{option}' does not exist!")

def get_section(section):
    section = section.lower()
    for config in configs:
        if section in config.dict.keys():
            return config.dict[section]

def set(option, value):
    option = option.lower()
    for config in configs:
        for section in config.dict.keys():
            if option in config.dict[section].keys():
                config.dict[section][option] = value
                return True
    logging.warning(f"Option '{option}' does not exist and cannot be updated.")
    return False