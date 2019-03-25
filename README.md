# xwillmarktheBot

A Twitch bot for (Ocarina of Time) Speedrunners by [xwillmarktheplace](https://twitch.tv/xwillmarktheplace). It can lookup world records and pb's on [Speedrun.com](https://www.speedrun.com/), provide information about your ongoing [SRL](http://www.speedrunslive.com/) race, summarize recent SRL results and post the hints you found in your randomizer playthrough. 

## Installation
To run the bot, you need Python 3.7. The bot was created on Windows and has not been tested for any other platform.

1. Get [Python 3.7](https://www.python.org/downloads/release/python-370/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html). The chatbot might run on older versions as well, but I did not test this and used newer Python features.
2. You need a Twitch account for the bot to send messages. Make one if you don't have one. Don't forget to make the account a mod or vip in your chat so it can send messages fast.
3. Generate an OAuth token for the bot account, which can be done [here](https://twitchapps.com/tmi/)
4. Download the program (in releases?)
5. Unzip the file wherever you want on your computer.

## Run the bot
You need to use your Python (3.7) installation to run the bot. This can be by done using one of the following methods.
* Run Main.py from the command prompt. You need to add the bot account's OAuth token as an argument and run as a module. If youn run from  Example:
``````
