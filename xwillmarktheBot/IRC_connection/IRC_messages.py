from xwillmarktheBot.IRC_connection.Twitch import Twitch_IRC
from xwillmarktheBot.Message_distributor import Message_distributor
from xwillmarktheBot.Settings import Settings
import re
import socket
import logging


class IRC_message_handler:

    def __init__(self, OAUTH):
        self.OAUTH = OAUTH
        self.irc = Twitch_IRC(Settings.STREAMER, Settings.BOT, OAUTH)

        self.timeouts = 0


    def run_irc_chat(self):
        self.irc.send_message("Bot succesfully connected.")
        self.chatbot = Message_distributor(self.irc)

        while (True):


            #try:
            if not self.irc.is_connected():
                return

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
                    sender = self.extract_sender(line[0])
                    self.parse_message(msg, sender)

            #
            # except (socket.error, socket.timeout) as e:
            #     logging.warning(f"IRC Socket error: {repr(e)}.")
            #     if not self.reconnect_irc():
            #         return logging.critical("Unable to reconnect, shutting down chatbot.")
            #
            # except Exception as e:
            #     logging.critical(f"Other exception in IRC: {repr(e)}")
            #     logging.critical(f"In message: {line}")
            #     logging.error(traceback.format_exc())
            #     self.irc.send_message("Error occured, please try a different command.")


    def extract_sender(self, msg):
        """Extract sender from message. Returns None if none is found."""
        match = re.search(r"(?<=:)\w+(?=!)", msg)
        if match:
            return match.group()

    def extract_message(self, msg):
        """Extract message from data. Located from 3rd position in list, then get rid of starting ':' """
        return ' '.join(msg[3:])[1:]

    def parse_message(self, msg, sender):
        logging.info(f"Received message from {sender}: {msg}")
        msg = msg.lower()

        if msg == "!throw_error":
            raise ValueError("test error")
        elif msg == "!throw_socket":
            raise socket.error("test socket died")

        self.chatbot.find_command(msg, sender)

    def reconnect_irc(self):
        if self.timeouts < 5:
            self.timeouts = self.timeouts + 1
            logging.critical(f"Attempting to reconnect (try {self.timeouts}).")
            self.irc = Twitch_IRC(Settings.STREAMER, Settings.BOT, self.OAUTH)

            #self.test = 1
            return True
        else:
            return False