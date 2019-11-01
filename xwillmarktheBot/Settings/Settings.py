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
# You could add your moderators. The STREAMER has to be in the list. Example: [STREAMER, 'user1', 'user2']
EDITORS  = [STREAMER]


# COMMAND SETTINGS
# ================
# Select which command sets to use.
# Set to False to disable a module for the bot

GENERAL      = True
SPEEDRUN_COM = True    # !pb, !wr, !userpb
SRL_RACES    = False    # !race, !card, !entrants, !goal
SRL_RESULTS  = True    # !average, !median, !results,
RANDO        = False    # !hints, !resethints



# SPEEDRUNSLIVE SETTINGS
# ================

# What type of races should the bot use for !average, !median and !results?
DEFAULT_RACE_TYPE = 'bingo'  # options: 'bingo', 'blackout', 'short-bingo', 'rando', 'other', 'srl'

# Each race type containing the word 'bingo' only considers races after this date.
# Put the date of the latest bingo version (for example v9.3), or leave an empty string '' if you always want all races.
# The date will usually only affect the !pb command for races.
# Format: 'DD-MM-YYYY'
LATEST_BINGO_VERSION_DATE = '09-06-2018'


# Whether the entrants should be printed along with the SRL link when using the !race command
# (Entrants can also be printed with !entrants)
PRINT_RACE_ENTRANTS = True


# If True, the commands likes !pb, !wr, !average, !results will respond by looking at the data of the person
# that posted the command. If set to False, the streamer defined above will be used by default.
RESPOND_TO_USER = True












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
CONSOLE_LOGGING_LEVEL = logging.INFO


# RANDO HINTS
# =================

# Location of rando hint files! Please keep their names at default (rando_hints.txt and rando_hints_template.txt)
# If you'd like to change the location, put a string with the full path to the folder containing those two files.
RANDO_HINTS_DIR = Definitions.ROOT_DIR / 'randohints'


# ALTERNATIVE USER LOOKUP NAMES
# =================

# In case you want to be able to find users based on any alt names they may use, you can add entries to
# this dictionary. The 'key' for each entry has to be their SRL user name, and the 'value' a list of one
# or more alt names.
ALT_NAMES = {
    'Kintefleush' : ['Fleush', 'Kinte', 'Happyfleush', 'Bleush', 'LeBleush'],
    'MooseOoT' : ['Moose', 'Moose_OoT']
}








