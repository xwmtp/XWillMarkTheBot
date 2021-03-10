from xwillmarktheBot.Connections.IRC_connection.IRC import IRC_connection
from xwillmarktheBot.Connections.IRC_connection.Connection import Connection_manager
from xwillmarktheBot.Connections.Discord_connection import Discord_connection
from xwillmarktheBot.Bot import Bot
from xwillmarktheBot.Config.Validate_settings import validate_settings
from xwillmarktheBot.Config import Configs
from xwillmarktheBot.Logger import initalize_logger

import os
import logging


if __name__ == '__main__':

    connection_type = Configs.connection_type

    def print_introduction():
        print("\n                _ _ _                      _    _   _          ____        _    \
               \n               (_) | |                    | |  | | | |        |  _ \      | |   \
               \n__  ____      ___| | |_ __ ___   __ _ _ __| | _| |_| |__   ___| |_) | ___ | |_  \
               \n\ \/ /\ \ /\ / / | | | '_ ` _ \ / _` | '__| |/ / __| '_ \ / _ \  _ < / _ \| __| \
               \n >  <  \ V  V /| | | | | | | | | (_| | |  |   <| |_| | | |  __/ |_) | (_) | |_  \
               \n/_/\_\  \_/\_/ |_|_|_|_| |_| |_|\__,_|_|  |_|\_\\\__|_| |_|\___|____/ \___/ \__|\
               \n\nWelcome to xwillmarktheBot by xwillmarktheplace. \
               \nPlease read the manual at https://github.com/xwmtp/xwillmarktheBot/blob/master/README.md for information/help.\n")

    if not os.path.exists(f'Settings/Settings-{connection_type}.ini'):
        Configs.create_settings()
        print_introduction()
        print(f"BEFORE USE:\
              \nA file Settings-{connection_type}.ini has been created in the Settings folder (xwillmarktheBot/Settings/Settings.ini).\
              \nPlease open the file in a text editor and fill in your personal settings (channel name, bot name, which modules you would like to use, etc).\
              \nThen restart this program to activate the bot.")
    else:
        Configs.import_settings()
        validate_settings()
        initalize_logger()

        print_introduction()

        if connection_type == 'twitch':
            connection = IRC_connection(Configs.get('streamer'), Configs.get('bot'), Configs.get('bot_oauth'))
            if connection.is_connected():
                connection_manager = Connection_manager(connection)
                bot = Bot(connection_manager)
                bot.run()
        if connection_type == 'discord':
            logging.info('Starting Discord bot.')
            bot = Discord_connection()
            bot.run()