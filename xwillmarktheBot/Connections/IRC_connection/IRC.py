import socket
import logging
import re

class IRC_connection:

    def __init__(self, channel_name, bot_name, bot_oauth):
        self.HOST = "irc.twitch.tv"
        self.PORT = 6667
        self.TIMEOUT = 10
        self.CHAN = "#" + channel_name
        self.NICK = bot_name
        self.PASS = bot_oauth
        self.socket = self.setup_connection()

    def setup_connection(self):
        try:
            con = socket.socket()
            con.settimeout(self.TIMEOUT)
            con.connect((self.HOST, self.PORT))

            # Send nickname, password (OAUTH) and join channel.
            logging.info(f"Connecting to bot account {self.NICK}.")
            con.send(bytes('PASS %s\r\n' % self.PASS, 'UTF-8'))
            con.send(bytes('NICK %s\r\n' % self.PASS, 'UTF-8'))
            logging.info(f"Joining channel {self.CHAN}.")
            con.send(bytes('JOIN %s\r\n' % self.CHAN, 'UTF-8'))
            con.send(bytes('CAP REQ :twitch.tv/tags\r\n', 'UTF-8'))

            logging.info('Finished setting up connection.')
            return con

        except Exception as e:
            logging.critical(
                f"Failed connecting to bot {self.NICK} and/or joining channel {self.CHAN}. Error: {repr(e)}")

    def reset_connection(self):
        self.socket = None
        self.socket = self.setup_connection()

    def is_connected(self):
        return self.socket is not None

    def send_pong(self, msg):
        self.socket.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))

    def send_ping(self, msg):
        self.socket.send(bytes('PING %s\r\n' % msg, 'UTF-8'))

    def send_message(self, msg):
        if msg == 'SOCKET':
            raise socket.error
        if isinstance(msg, list):
            for m in msg:
                self.socket.send(bytes('PRIVMSG %s :%s\r\n' % (self.CHAN, m), 'UTF-8'))
        else:
            self.socket.send(bytes('PRIVMSG %s :%s\r\n' % (self.CHAN, msg), 'UTF-8'))
        logging.info(f"Sent message: {msg}")

    def part_channel(self):
        self.socket.send(bytes('PART %s\r\n' % self.CHAN, 'UTF-8'))

    def receive_data(self, characters=2048):
        return self.socket.recv(characters).decode('UTF-8')

    def to_message(self, line):
        return IRC_message(line)


class IRC_message:

    def __init__(self, raw_message):
        message_parts = str.rstrip(raw_message).split(' ')
        logging.debug(f"to parse: {message_parts}")
        if message_parts[0][0] == '@':
            self.tag = message_parts[0]
            message_parts = message_parts[1:]
        else:
            self.tag = None
        self.irc_message = ' '.join(message_parts)
        self.client_identifier = message_parts[0]
        self.command = message_parts[1]
        self.recipient = message_parts[2]
        self.content = ' '.join(message_parts[3:])[1:]
        self.KNOWN_COMMANDS = ['PRIVMSG', 'JOIN', 'PING', 'PONG', 'CAP']
        logging.debug(
            f'Parsed tag {self.tag}, client {self.client_identifier}, command {self.command}, rec {self.recipient}, content {self.content}')

    def sender(self):
        if self.command == 'PRIVMSG':
            match = re.search(r"(?<=:)\w+(?=!)", self.client_identifier)
            if match:
                return match.group()

    def is_private_message(self):
        return self.command == 'PRIVMSG'

    def is_ping(self):
        return self.command == 'PING'

    def is_pong(self):
        return self.command == 'PONG'

    def is_unknown(self):
        if self.command in self.KNOWN_COMMANDS:
            return False
        try:
            int(self.command)
            return True
        except ValueError:
            return False

    def log(self, level='info'):
        if level=='warning:':
            logging.warning(f"Message: {self.irc_message}")
        else:
            logging.info(f"Message: {self.irc_message}")