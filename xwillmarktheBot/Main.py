from xwillmarktheBot.IRC_connection.IRC_messages import IRC_message_handler
import logging
import sys

def initalize_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')


    # console handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # file handler (errors)
    handler = logging.FileHandler("logs/ERROR_log.log", "a")
    handler.setLevel(logging.WARNING)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # file handler (info)
    handler = logging.FileHandler("logs/INFO_log.log", "a")
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)







if __name__ == '__main__':


    initalize_logger()


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





