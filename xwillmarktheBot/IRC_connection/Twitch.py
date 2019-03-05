import socket
import logging

class Twitch_IRC:

    def __init__(self, channel_name, bot_name, bot_oauth):
        self.HOST = "irc.twitch.tv"
        self.PORT = 6667
        self.CHAN = "#" + channel_name
        self.connection = self.setup_connection(bot_name, bot_oauth)

    def setup_connection(self, nickname, password):
        try:
            con = socket.socket()
            con.connect((self.HOST, self.PORT))

            # Send nickname, password (OAUTH) and join channel).
            logging.info(f"Connecting to bot {nickname}.")
            logging.info(f"Joining channel {self.CHAN}.")
            con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))
            con.send(bytes('NICK %s\r\n' % nickname, 'UTF-8'))
            con.send(bytes('JOIN %s\r\n' % self.CHAN, 'UTF-8'))

            return con

        except Exception as e:
            logging.critical(f"Failed connecting to bot {nickname} and or joining channel {self.CHAN}. Error: {repr(e)}")
            logging.info("Check internet connection.")


    def is_connected(self):
        return self.connection is not None




    def send_pong(self, msg):
        self.connection.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))

    def send_message(self, msg):
        logging.info("Sent message: " + msg)
        self.connection.send(bytes('PRIVMSG %s :%s\r\n' % (self.CHAN, msg), 'UTF-8'))

    def part_channel(self):
        self.connection.send(bytes('PART %s\r\n' % self.CHAN, 'UTF-8'))

    def receive_data(self, characters = 1024):
        logging.debug(f"Receiving irc data ({characters} characters)...")
        return self.connection.recv(characters).decode('UTF-8')