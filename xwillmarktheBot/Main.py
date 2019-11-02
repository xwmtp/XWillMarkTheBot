from xwillmarktheBot.IRC_connection.IRC_messages import IRC_message_handler
from xwillmarktheBot.Settings import Settings
from xwillmarktheBot.Settings.Validate_settings import validate_settings
from xwillmarktheBot.Settings.Manage_settings import *
from xwillmarktheBot.Logger import initalize_logger
import os
import sys


if __name__ == '__main__':

    def print_introduction():
        print("\n                _ _ _                      _    _   _          ____        _    \
               \n               (_) | |                    | |  | | | |        |  _ \      | |   \
               \n__  ____      ___| | |_ __ ___   __ _ _ __| | _| |_| |__   ___| |_) | ___ | |_  \
               \n\ \/ /\ \ /\ / / | | | '_ ` _ \ / _` | '__| |/ / __| '_ \ / _ \  _ < / _ \| __| \
               \n >  <  \ V  V /| | | | | | | | | (_| | |  |   <| |_| | | |  __/ |_) | (_) | |_  \
               \n/_/\_\  \_/\_/ |_|_|_|_| |_| |_|\__,_|_|  |_|\_\\\__|_| |_|\___|____/ \___/ \__|\
               \n\nWelcome to xwillmarktheBot by xwillmarktheplace. \
               \nPlease read the manual at https://github.com/xwmtp/xwillmarktheBot/blob/master/README.md for information/help.\n")

    if not os.path.exists('Settings.py'):
        create_settings()
        print_introduction()
        print("BEFORE USE:\
              \nA file Settings.py has been created in the root folder (xwillmarktheBot/Settings.py).\
              \nPlease open the file in a text editor fill in your personal settings (including channel name, bot name, which modules you would like to use, etc).\
              \nThen restart this program to activate the bot.")
    else:
        copy_settings()
        validate_settings()
        initalize_logger()

        print_introduction()

        bot = IRC_message_handler(Settings.BOT_OAUTH)
        if bot.irc.is_connected():
            bot.run_irc_chat()


# IDEAS
# - most common word in comments?
# - derive most common row from comments





