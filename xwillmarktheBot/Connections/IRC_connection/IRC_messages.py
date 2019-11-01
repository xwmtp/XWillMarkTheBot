from xwillmarktheBot.Connections.IRC_connection.Twitch import Twitch_IRC
from xwillmarktheBot.Message_distributor import Message_distributor
from xwillmarktheBot.Settings import Settings
import traceback
import re
import socket
import logging
import time

PING_TIMEOUT = 15

class IRC_message_handler:

    def __init__(self, OAUTH):
        self.OAUTH = OAUTH
        self.irc = Twitch_IRC(Settings.STREAMER, Settings.BOT, OAUTH)

        self.connected = False
        self.timeouts = 0
        self.last_ping_sent = time.time()
        self.waiting_for_pong = False



    def run_irc_chat(self):
        self.chatbot = Message_distributor(self.irc)
        data = ''
        while (True):
            try:

                self.check_connection()

                logging.info("\n\nNew irc message:\n-------------------")
                data = self.irc.receive_data()

                if data:
                    self.parse_data(data)


            except socket.timeout as e:
                logging.info(f'Did not receive data after {self.irc.connection.gettimeout()} seconds.')
                if self.waiting_for_pong:
                    logging.critical(f"Did not receive PONG since last timeout, trying to reconnect..")
                    self.waiting_for_pong = False
                    self.reconnect_irc()
                else:
                    self.send_ping()

            except socket.error as e:
                logging.critical(f"IRC Socket error: {repr(e)}.")
                self.reconnect_irc()

            except Exception as e:
                logging.critical(f"Other exception in IRC: {repr(e)}")
                logging.critical(f"In message: {data}")
                logging.error(traceback.format_exc())
                self.irc.send_message("Error occured, please try a different command.")



    def parse_data(self, data):
        # split on new lines, get rid of empty '' in the end

        def extract_sender(msg):
            """Extract sender from message. Returns None if none is found."""
            match = re.search(r"(?<=:)\w+(?=!)", msg)
            if match:
                return match.group()

        def extract_message(msg):
            """Extract message from data. Located from 3rd position in list, then get rid of starting ':' """
            return ' '.join(msg[3:])[1:]


        data_lines = re.split(r"[\r\n]+", data)[:-1]

        for line in data_lines:
            logging.debug(line)
            words = str.rstrip(line).split(' ')

            if len(words) > 0:
                msg = extract_message(words)

                if words[0] == 'PING':
                    logging.info('Received PING.')
                    self.irc.send_pong(line[1])

                elif words[1] == 'PONG':
                    logging.info('Received PONG.')
                    self.waiting_for_pong = False

                elif words[1] == 'PRIVMSG':
                    sender = extract_sender(words[0])
                    self.parse_message(msg, sender)

                elif words[1] == 'NOTICE':
                    logging.warning(f"Received NOTICE: {msg}")
                    if msg == 'Login authentication failed':
                        logging.critical(msg)
                        logging.critical("Please check if OAuth token is correct.")
                        return False

                else:
                    logging.info(f"Received other message: {msg}")
                    self.check_first_connection(words)

        return True

    def check_connection(self):
        if not self.irc.is_connected():
            return self.reconnect_irc()

        time_since_ping = time.time() - self.last_ping_sent

        if time_since_ping > PING_TIMEOUT:
            if self.waiting_for_pong:
                logging.critical(f"Received no PONG after {PING_TIMEOUT} seconds, trying to reconnect.")
                self.reconnect_irc()
                return True
            else:
                self.send_ping()
                return True



    def parse_message(self, msg, sender):
        logging.info(f"Received message from {sender}: {msg}")
        msg = msg.lower()

        if msg == "!throw_error":
            raise ValueError("test error")
        elif msg == "!throw_socket":
            raise socket.error("test socket died")

        self.chatbot.find_command(msg, sender)

    def check_first_connection(self, words):
        if not self.connected and words[0].startswith(':' + Settings.BOT.lower()):
            logging.info('Sucesfully connected to irc.')
            self.irc.send_message('Succesfully connected.')
            self.connected = True

    def send_ping(self):
        self.last_ping_sent = time.time()
        self.irc.send_ping('checking_connection')
        self.waiting_for_pong = True



    def reconnect_irc(self):
        attempts = 0
        interval = 2 # seconds before next attempt

        while True:
            attempts += 1

            if attempts > 5:
                logging.info(f"Waiting {interval} seconds before reconnect...")
                time.sleep(interval)
                interval = interval * 2

            logging.critical(f"Attempting to reconnect (attempt {attempts}).")
            self.irc = Twitch_IRC(Settings.STREAMER, Settings.BOT, self.OAUTH)
            if self.irc.is_connected():
                return True