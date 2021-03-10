from xwillmarktheBot.Connections.IRC_connection.IRC import IRC_connection
from xwillmarktheBot.Connections.IRC_connection.Connection import setup_and_run_irc
from xwillmarktheBot.Connections.Discord_connection import setup_and_run_discord
from xwillmarktheBot.Config.Validate_settings import validate_settings
from xwillmarktheBot.Config import Configs
from xwillmarktheBot.Logger import initalize_logger
import os

def print_introduction():
    print("\n                _ _ _                      _    _   _          ____        _    \
           \n               (_) | |                    | |  | | | |        |  _ \      | |   \
           \n__  ____      ___| | |_ __ ___   __ _ _ __| | _| |_| |__   ___| |_) | ___ | |_  \
           \n\ \/ /\ \ /\ / / | | | '_ ` _ \ / _` | '__| |/ / __| '_ \ / _ \  _ < / _ \| __| \
           \n >  <  \ V  V /| | | | | | | | | (_| | |  |   <| |_| | | |  __/ |_) | (_) | |_  \
           \n/_/\_\  \_/\_/ |_|_|_|_| |_| |_|\__,_|_|  |_|\_\\\__|_| |_|\___|____/ \___/ \__|\
           \n\nWelcome to xwillmarktheBot by xwillmarktheplace. \
           \nPlease read the manual at https://github.com/xwmtp/xwillmarktheBot/blob/master/README.md for information/help.\n")

def print_instructions():
    print(f"BEFORE USE:\
          \nA file Settings-{connection_type}.ini has been created in the Settings folder (xwillmarktheBot/Settings/Settings.ini).\
          \nPlease open the file in a text editor and fill in your personal settings (channel name, bot name, which modules you would like to use, etc).\
          \nThen restart this program to activate the bot.")


if __name__ == '__main__':
    connection_type = Configs.connection_type

    first_time_boot = not os.path.exists(f'Settings/Settings-{connection_type}.ini')
    if first_time_boot:
        Configs.create_settings()
        print_introduction()
        print_instructions()
    else:
        Configs.import_settings()
        validate_settings()
        initalize_logger()

        print_introduction()

        if connection_type == 'twitch':
            setup_and_run_irc()

        if connection_type == 'discord':
            setup_and_run_discord()
