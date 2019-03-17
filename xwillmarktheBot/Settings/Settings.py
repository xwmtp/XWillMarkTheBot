from xwillmarktheBot.Settings import Definitions
import logging


#=======================#
#       SETTINGS        #
#=======================#

# May be edited by the user!


# STREAM SETTINGS
# ================

STREAMER = 'xwillmarktheplace'
BOT      = 'xwillmarktheBot'

# Editors are Twitch users with rights to use all commands (like resetting rando hints)
EDITORS  = [STREAMER, 'scaramangado', 'jelster64', 'juwk']


# COMMAND SETTINGS
# ================
# Select which command sets to use.
# Set to False to disable a module for the bot

SPEEDRUN_COM = True    # !pb, !wr, !userpb
SRL_RACES    = True    # !race, !card, !entrants, !goal
SRL_RESULTS  = True    # !average, !median, !results,



# SPEEDRUNSLIVE SETTINGS
# ================

# What type of races should the bot use for !average, !median and !results?
DEFAULT_RESULT_TYPE = 'bingo'  # options: 'bingo', 'blackout', 'short-bingo', 'rando', 'other'


# Whether the entrants should be printed along with the SRL link when using the !race command
# (Entrants can also be printed with !entrants)
PRINT_RACE_ENTRANTS = True











#=======================#
#   ADVANCED SETTINGS   #
#=======================#


# LOGGING
# ================

# Amount of messages sent to your bot console.
# Options:
# logging.DEBUG    all messages, including ones meant for development (like information about api requests, used functions, etc)
# logging.INFO     recommended level. information about sent and received messages, and warning/errors
# logging.WARNING  only warnings and errors
# logging.ERROR    only errors
CONSOLE_LOGGING_LEVEL = logging.DEBUG


# RANDO HINTS
# =================

# Location of rando hint files! Please keep their names at default (rando_hints.txt and rando_hints_template.txt)
# If you'd like to change the location, put a string with the full path to the folder containing those two files.
RANDO_HINTS_DIR = Definitions.ROOT_DIR / 'RandoHints'













