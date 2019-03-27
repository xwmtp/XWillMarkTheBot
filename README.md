# xwillmarktheBot

A Twitch bot for (Ocarina of Time) Speedrunners by [xwillmarktheplace](https://twitch.tv/xwillmarktheplace). It can lookup world records and pb's on [Speedrun.com](https://www.speedrun.com/), provide information about your ongoing [SRL](http://www.speedrunslive.com/) race, summarize recent SRL results and post the hints you found in your randomizer playthrough. 

## Installation
To run the bot, you need Python 3.7. The bot was created on Windows and has not been tested for any other platform.

1. Get [Python 3.7](https://www.python.org/downloads/release/python-370/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html). The chatbot might run on older versions as well, but I did not test this and used newer Python features.
2. You need a Twitch account for the bot to send messages. Make one if you don't have one. Don't forget to make the account a mod or vip in your chat so it can send messages fast.
3. Generate an OAuth token for the bot account, which can be done [here](https://twitchapps.com/tmi/)
4. Download the program (in releases?)
5. Unzip the file wherever you want on your computer.

## Running
You need to use your Python (3.7) installation to run the bot. This can be by done using one of the following methods.
* Run Main.py from the command prompt. You need to add the bot account's OAuth token as an argument and run as a module. Example:
```python -m xwillmarktheBot.Main oauth:123test```

## Settings
The bot has a few settings that can be adjusted. They can all be found in ```xwillmarktheBot/Settings/Settings.py```.
### Stream
* **Streamer**: the name of the twitch channel where the bot should reside
* **Bot**: the user name of the bot account on twitch
* **Editors**: list of twitch users with extra permissions. It's advised to put your channel moderators here, but it's up to you. The streamer always has to be in here too (as they are by default)!

### Command modules
You can deactivate command modules that you don't want to use in your bot. By default, all modules are activated with the keyword ```True```. Put ```False``` for any module you don't want to use.
* **Speedrun_com**: commands to look up records on Speedrun.com, like *!pb*, *!wr* and *!userpb*.
* **SRL_races**: ccommands for ongoing SRL races, like *!race*, *!entrants* and *!goal*.
* **SRL_results**: commands to get information about past races, like *!average*, *!results* and *!pb*.

### Speedrunslive
* **Default_race_type**: pick the default type of srl race you want the SRL results module to work on. You can pick from *bingo*, *blackout*, *short-bingo*, *rando*, *other* and *all*. By default this will be set to *bingo*. Note that the default can be changed while the program is running, but when the bot restarts it will use the default in the settings file again. It's possible to get information about non-default race types by adding arguments.
* **Print_race_entrants**: when set to *True*, the commands *!race* will print all the race entrants in addition to the SRL race url. If you don't want this behavior (for example if you often race with a large amount of entrants), you can set this to *False*. Note that you can always use *!entrants* to print all the entrants, as long as it fits within one twitch chat message!

## Commands
A nice overview of all commands that can be used with the bot can be found [here](https://xwmtp.github.io/xwillmarktheBot). It also explains the usage of the commands.

