from xwillmarktheBot.Command_handler import Chatbot
from xwillmarktheBot.IRC_connection.IRC_messages import IRC_message_handler
import logging
import sys

if __name__ == '__main__':

    if len(sys.argv) < 2:
        logging.critical('No OAUTH provided, please provide it as a sys arg.')
    else:
        oauth = sys.argv[1]

    logging.basicConfig(level=logging.DEBUG)



    bot = IRC_message_handler(oauth)
    bot.run_irc_chat()


# IDEAS
# - most common word in comments?
# - derive most common row from comments