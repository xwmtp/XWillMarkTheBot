from xwillmarktheBot.IRC_connection.IRC_messages import IRC_message_handler
from xwillmarktheBot.Settings.Validate_settings import validate_settings
from xwillmarktheBot.Logger import initalize_logger
import sys


if __name__ == '__main__':


    initalize_logger()
    validate_settings()


    if len(sys.argv) < 2:
        raise ValueError('No OAUTH provided, please provide it as a sys arg.')
    else:
        oauth = sys.argv[1]


    bot = IRC_message_handler(oauth)
    if bot.irc.is_connected():
        bot.run_irc_chat()


# IDEAS
# - most common word in comments?
# - derive most common row from comments





