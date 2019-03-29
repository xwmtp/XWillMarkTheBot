# xwillmarktheBot

A Twitch bot for (Ocarina of Time) Speedrunners by [xwillmarktheplace](https://twitch.tv/xwillmarktheplace). It can lookup world records and pb's on [Speedrun.com](https://www.speedrun.com/), provide information about your ongoing [SRL](http://www.speedrunslive.com/) race, summarize recent SRL results and post the hints you found in your randomizer playthrough. 

## Installation
To run the bot, you need Python 3.7. The bot was created on Windows and has not been tested for any other platform.

1. Get [Python 3.7](https://www.python.org/downloads/release/python-370/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html). The chatbot might run on older versions as well, but I did not test this and used newer Python features.
2. You need a Twitch account for the bot to send messages. Make one if you don't have one. Don't forget to make the account a mod or vip in your chat so it can send messages fast.
3. Generate an OAuth token for the bot account, which can be done [here](https://twitchapps.com/tmi/). Don't share this token!
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
* **Speedrun_com**: commands to look up records on Speedrun.com, like ```!pb```, ```!wr``` and ```!userpb```.
* **SRL_races**: ccommands for ongoing SRL races, like ```!race```, ```!entrants``` and ```!goal```.
* **SRL_results**: commands to get information about past races, like ```!average```, ```!results``` and ```!pb```.

### Speedrunslive
* **Default_race_type**: pick the default type of srl race you want the SRL results module to work on. You can pick from ```bingo```, ```blackout```, ```short-bingo```, ```rando```, ```other``` and ```all```. By default this will be set to ```bingo```. Note that the default can be changed while the program is running, but when the bot restarts it will use the default in the settings file again. It's possible to get information about non-default race types by adding arguments.
* **Latest_bingo_version_date**: if you want the !pb command to only consider races from the latest bingo version, put the date here that the latest version came out, formatted like 'DD-MM-YYYY'. Put an empty string '' if you always want all races to be considered. This wil only influence race types that have the word 'bingo' in them. If you put a date here but sometimes want to look up all the bingos, you can put 'all-' in front of the bingo type. For example: ```!pb all-bingo```.
* **Print_race_entrants**: when set to ```True```, the command ```!race``` will print all the race entrants in addition to the SRL race url. If you don't want this behavior (for example if you often race with a large amount of entrants), you can set this to ```False```. Note that you can always use ```!entrants``` to print all the entrants, as long as it fits within one twitch chat message!

## Commands
A nice overview of all commands that can be used with the bot can be found [here](https://xwmtp.github.io/xwillmarktheBot). It also explains the usage of the commands. Using ```!commands``` will return a link to that page.

### Speedrun.com
The Speedrun.com module contains commands to look up records and pb's.
* If you don't add an argument to ```!pb``` or ```!wr```, the bot will look at your current stream title. Everything between square brackets or after the | symbol will be ignored.
* If you look up a category which has subcategories like for example Glitchless, you get the first tab as a default answer. Add the subtab to find a specific subcategory. Example: ````!wr glitchless any% unrestricted```
* To get the pb of someone other than the streamer, use ````!userpb```. Example: ````!userpb scaramanga 37 water keys```. Again, not adding a category will result in looking at the stream title.

### SRL results
The SRL results module can look up statistics on *past* SRL races. There are a few types of races that the bot can distinguish. These are ```bingo```, ```short-bingo```, ```blackout```, ```rando```, ```other``` and ```srl```. The ```srl``` type means 'all' races.   
* If you use ```!pb```, the module will look if any of the above mentioned SRL race types are in your stream title. If not, it will send the title to the Speedrun.com module and look for an rta category instead. Of course you can also add an argument yourself, like ```!pb blackout``` if you want to find the best blackout race you did.
* The other SRL result commands (```!average```, ```!median``` and ```!results```) will use the default race type. You can set this in the settings file ```Settings.py```, or use the ```!setsrl``` command. It's possible to add an integer for how many races you want to consider, and a user name to get someone else's stats.

### SRL races
The SRL races module has commands to get information on a current race. The bot automatically looks at the race the streamer has entered.
* Use ```!race``` and ```!entrants``` to get info on your current race. If you don't want ```!race``` to show all the entrants (if you often join very large races for example), you can edit this in ```Settings.py```.


### Rando
The rando module allows you to have an up-to-date command with the hints you already found in your oot rando.
* While playing, have ```RandoHints/rando_hints.txt``` open in a text editor. Everytime you find a hint, double click on 'location' or 'item' and type what you find. Make sure to hit ctrl + s afterwards to save. When a viewer uses the ```!hints``` command, only the hints that you filled in will show up.
* After playing, use the ```!resethints``` command to restore the file to default. The contents of ```RandoHints/rando_hints_template.txt``` will be copied to the file, so it's strongly recommended to not change the template.
* It's possible to alter the template a bit to your own liking, by adding another group of hints with a different title. Keep it close to the template though (with ascending numbers and a semi-colon as a separator), or the code won't be able to parse it.
* You can put the two rando text files in a different directory if you'd like, but you have to put the path in the advanced settings of ```Settings.py```. The file names have to stay the same though!
