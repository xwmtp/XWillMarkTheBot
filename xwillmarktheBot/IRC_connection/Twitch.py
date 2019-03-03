from xwillmarktheBot.IRC_connection.IRC_messages import IRC_message_handler
import xwillmarktheBot.Settings as Settings
import socket
import logging

class Twitch_IRC:

    def __init__(self, channel_name, bot_name, bot_oauth):
        self.HOST = "irc.twitch.tv"
        self.PORT = 6667
        self.CHAN = "#" + channel_name
        self.connection = self.setup_connection(bot_name, bot_oauth)

    def setup_connection(self, nickname, password):
        con = socket.socket()
        con.connect((self.HOST, self.PORT))

        # Send nickname, password (OAUTH) and join channel).
        logging.info(f"Connecting to {nickname} with password {password}.")
        logging.info(f"Joining channel {self.CHAN}.")
        con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))
        con.send(bytes('NICK %s\r\n' % nickname, 'UTF-8'))
        con.send(bytes('JOIN %s\r\n' % self.CHAN, 'UTF-8'))

        return con


    def send_pong(self, msg):
        self.connection.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))

    def send_message(self, msg):
        logging.debug("Sent message: " + msg)
        self.connection.send(bytes('PRIVMSG %s :%s\r\n' % (self.CHAN, msg), 'UTF-8'))

    def part_channel(self):
        self.connection.send(bytes('PART %s\r\n' % self.CHAN, 'UTF-8'))

    def receive_data(self, characters = 1024):
        logging.debug(f"Receiving irc data ({characters} characters)")
        return self.connection.recv(characters).decode('UTF-8')


