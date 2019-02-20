from Chatbot import Chatbot
import logging

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    bot = Chatbot()

    #message = input("Chat message:").lower()
    message = "#srl-xk8w7"

    while(True):
        bot.find_command(message)
        message = input().lower()



# IDEAS
# - most common word in comments?
# - derive most common row from comments