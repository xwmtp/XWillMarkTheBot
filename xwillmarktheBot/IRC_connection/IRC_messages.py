from xwillmarktheBot.IRC_connection.Twitch import Twitch_IRC
from xwillmarktheBot.Command_handler import Command_handler
from xwillmarktheBot import Settings
import re
import socket
import logging

class IRC_message_handler:

    def __init__(self, OAUTH):
        self.irc = Twitch_IRC(Settings.STREAMER, Settings.BOT, OAUTH)
        self.chatbot = Command_handler(self.irc)


    def run_irc_chat(self):
        self.irc.send_message("Bot succesfully connected.")

        while (True):

            try:


                logging.debug("\n\nNew irc message:\n-------------------")

                data = self.irc.receive_data()
                data_lines = re.split(r"[~\r\n]+", data)[:-1]

                for line in data_lines:
                    logging.debug(line)
                    line = str.rstrip(line)
                    line = line.split(' ')

                    if len(line) == 0:
                        continue

                    if line[0] == 'PING':
                        self.irc.send_pong(line[1])

                    if line[1] == 'PRIVMSG':
                        msg = self.extract_message(line) # get rid of starting :
                        self.parse_message(msg)

            except socket.error:
                logging.warning("IRC Socket died.")

            except socket.timeout:
                logging.warning("IRC Socket timeout.")

            except Exception as e:
                logging.critical("Other exception in IRC:", e)
                self.irc.send_message("Error occured, please try a different command.")


    def extract_sender(self, msg):
        """Extract sender from message. Returns None if none is found."""
        match = re.search(r"(?<=:)\w+(?=!)", msg)
        if match:
            return match.group()

    def extract_message(self, msg):
        """Extract message from data. Located from 3rd position in list, then get rid of starting ':' """
        return ' '.join(msg[3:])[1:]

    def parse_message(self, msg):
        logging.debug("Parsing message: " + msg)
        msg = msg.lower()

        self.chatbot.find_command(msg)