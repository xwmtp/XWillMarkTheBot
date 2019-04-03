from xwillmarktheBot.IRC_connection.IRC_messages import IRC_message_handler
from xwillmarktheBot.Settings.Validate_settings import validate_settings
from xwillmarktheBot.Logger import initalize_logger
import logging
import sys


if __name__ == '__main__':

    if len(sys.argv) < 2:
        raise ValueError('No OAUTH provided, please provide it as a sys arg.')
    else:
        oauth = sys.argv[1]

    initalize_logger()
    validate_settings()


    print("\n                _ _ _                      _    _   _          ____        _    \
           \n               (_) | |                    | |  | | | |        |  _ \      | |   \
           \n__  ____      ___| | |_ __ ___   __ _ _ __| | _| |_| |__   ___| |_) | ___ | |_  \
           \n\ \/ /\ \ /\ / / | | | '_ ` _ \ / _` | '__| |/ / __| '_ \ / _ \  _ < / _ \| __| \
           \n >  <  \ V  V /| | | | | | | | | (_| | |  |   <| |_| | | |  __/ |_) | (_) | |_  \
           \n/_/\_\  \_/\_/ |_|_|_|_| |_| |_|\__,_|_|  |_|\_\\\__|_| |_|\___|____/ \___/ \__|\
           \n\nWelcome to xwillmarktheBot by xwillmarktheplace. \
           \nPlease read the manual at https://github.com/xwmtp/xwillmarktheBot/blob/master/README.md for information/help.\n")

    bot = IRC_message_handler(oauth)
    if bot.irc.is_connected():
        bot.run_irc_chat()


# IDEAS
# - most common word in comments?
# - derive most common row from comments





