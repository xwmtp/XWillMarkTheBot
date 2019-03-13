from xwillmarktheBot.Settings import Settings
import logging

def initalize_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')


    # console handler
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(Settings.CONSOLE_LOGGING_LEVEL)
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