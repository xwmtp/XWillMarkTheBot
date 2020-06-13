import logging
from pathlib import Path

# Definitions used for general settings. Should not be edited by user!


RACE_TYPES = ['bingo', 'all-bingo', 'blackout', 'short-bingo', 'all-short-bingo', 'rando', 'other', 'srl']

LOGGING_LEVELS = [logging.DEBUG, logging.INFO, logging.WARNING, logging.CRITICAL]

#ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT_DIR = Path(__file__).resolve().parent.parent.parent