# xwillmarktheBot

## Table of contents
-   [Introduction](#introduction)
-   [Installation](#installation)
-   [Running](#running)
    - [With bat script](#with-bat-script)
    - [From command line](#from-command-line)
-   [Settings](#settings)
    - [Stream](#stream)
    - [Command modules](#command-modules)
    - [SpeedRunsLive](#speedrunslive)
-   [Commands](#commands)
    - [Speedrun.com](#speedrun_com)
    - [SRL results](#srl-results)
    - [SRL races](#srl-races)
    - [Randomizer](#rando)


## Introduction
This is a Twitch bot developed for *Ocarina of Time* speedrunners, created by [xwillmarktheplace](https://twitch.tv/xwillmarktheplace). It includes various modules to provide viewers with information about your speedruns and races. Currently it can:

* Fetch up-to-date records from [Speedrun.com](https://www.speedrun.com/)
![src](https://github.com/xwmtp/xwillmarktheBot/blob/master/images/Speedrun_com.PNG)

* Post the goal and entrants of your current [SRL](http://www.speedrunslive.com/) race
![race](https://github.com/xwmtp/xwillmarktheBot/blob/master/images/Race.PNG)

* Return stats from past SRL races
![results](https://github.com/xwmtp/xwillmarktheBot/blob/master/images/Results.PNG)

* Keep track of hints found in oot rando
![Rando](https://github.com/xwmtp/xwillmarktheBot/blob/master/images/Rando.PNG)


## Installation
You need at least Python 3.7 to run the bot. The bot was created for **Windows** and has not been tested on any other platform.



1. Get [Miniconda3](https://docs.conda.io/en/latest/miniconda.html) (with at least Python 3.7). If you use your own Python installation, you might have to install packages to make it work.
2. You need a Twitch account for the bot to send messages. Make one if you don't have one. Don't forget to make the account a mod or vip in your chat so it can send messages fast.
3. Generate an **OAuth** token for the bot account, which can be done [here](https://twitchapps.com/tmi/). Don't share this token!
4. Download the program (in releases?) and unzip the folder wherever you want on your computer.
6. Go to ```xwillmarktheBot/Settings/Settings.py``` and add your Twitch account and that of your bot. Go to [Settings](#settings) for more information on the different settings. 

## Running
You need to use your Python (3.7) installation to run the bot. You can use the included bat script to run the bot, or run it yourself from the command line.

### With bat script
1. Open ```run.bat``` in a text editor. Replace the default ```oauth:test123``` with your bot account's OAuth token (generated during the [installation](#installation)).
2. Double click ```run.bat``` to run the bot.

If you get an error, you may have multiple Python installations on your computer and the wrong one might be used. In that case, open the bat file in a text editor and replace ```python``` with the path to your Python 3.7 installation, for example: ```C:\Users\<user>\Anaconda3\python.exe```

### From command line
1. Open a command prompt (cmd or the anaconda prompt)
2. Go to the bot's folder. Example: ```cd C:\Users\<user>\Documents\xwillmarktheBot```
3. Run the main file as follows, adding your bot's OAuth token as an argument: ```python -m xwillmarktheBot.Main oauth:123test``` 

If you have trouble running the bot, please contact me.

## Settings
The bot has a few settings that can be adjusted. They can all be found in ```xwillmarktheBot/Settings/Settings.py```.
### Stream
These settings have to be changed in order to run the bot!
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
A nice overview of all commands that can be used with the bot can be found [here](https://xwmtp.github.io/xwillmarktheBot). It also explains the usage of the commands. Using ```!commands``` will return a link to that page so your viewers will know what and how to use. Below are a few additions to the command overview page that might be important for you as the streamer.

### Speedrun_com
The *Speedrun.com* module contains commands to look up records and pb's.
* If you don't add an argument to ```!pb``` or ```!wr```, the bot will look at your current stream title. Everything between square brackets or after the | symbol will be ignored.
* If you look up a category which has subcategories like Glitchless, you get the first subtab as the default answer. Add a subtab name to find a specific subcategory. Example: ```!wr glitchless any% unrestricted```
* To get the pb of someone other than the streamer, use ```!userpb```. Example: ```!userpb scaramanga 37 water keys```. Again, not adding a category will result in looking at the stream title.
* If you want the bot to find correct categories in your stream title, make sure the title starts with the category name.

### SRL results
The *SRL results* module can look up statistics from *past* SRL races. There are a few types of races that the bot can distinguish. These are ```bingo```, ```short-bingo```, ```blackout```, ```rando```, ```other``` and ```srl```. The ```srl``` type stands for *all* races.   
* If you use ```!pb```, the module will look if any of the above mentioned SRL race types are in your stream title. If not, it will send the title to the Speedrun.com module and look for an rta category instead. Of course you can also add an argument yourself, like ```!pb blackout``` if you want to find the best blackout race you did.
* The other SRL result commands (```!average```, ```!median``` and ```!results```) will use the default race type. You can [set](#speedrunslive) this in the settings file ```Settings.py```, or use the ```!setsrl``` command to change it.
* The bingo race types (```bingo```, ```short-bingo```, ```blackout```) will only look at oot races.
* For race types ```bingo``` and ```short-bingo```, only races after the 'latest bingo version date' in the [settings](#speedrunslive) will be considered. If you want to look at all races instead, either delete the date in the settings or add ```all-``` in front of the type. Example: ```!average all-short-bingo```

### SRL races
The *SRL races* module has commands to get information on a current race. The bot automatically finds which SRL race the streamer has entered.
* Use ```!race```, ```!goal``` ```!entrants``` to get info on your current race. If you don't want ```!race``` to show all the entrants (for example if you often join very large races), you can change this [setting](#speedrunslive) in ```Settings.py```.
* The ```!card``` command will only return the goal if the current race is classified as a bingo.


### Rando
The *randomizer* module allows you to have an up-to-date command with the hints you already found in your (oot) randomizer.
* To use the rando hints command, you need to have ```RandoHints/rando_hints.txt``` open in a text editor while playing. Everytime you find a hint, double click on 'location' or 'item' and type what you found. Don't worry about extra spaces. Make sure to hit ctrl + s afterwards to save the file. When a viewer uses the ```!hints``` command, only the hints that you filled in will show up.
* After playing, use the ```!resethints``` command to restore the file to default. The contents of ```RandoHints/rando_hints_template.txt``` will be copied to the file, so it's recommended to not change the template.
* It's possible to alter the template a bit to your own liking, by adding another group of hints with a different title. Stay close to the original template though (with ascending numbers and a semi-colon as a separator), or the code won't be able to parse it.
* You can put the two rando text files in a different directory if you'd like, but you have to put the path in the advanced settings of ```Settings.py```. The file names have to stay the same though!
