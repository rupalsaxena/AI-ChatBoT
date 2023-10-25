import csv
from datetime import datetime
from speakeasypy import Speakeasy, Chatroom
from typing import List
import time
from Algorithm import getResponse
from Preprocess import Preprocess
from utils import log_to_csv

DEFAULT_HOST_URL = 'https://speakeasy.ifi.uzh.ch'
listen_freq = 2
DEFAULT_MSG = "I don't understand you. Can you rephrase it?"
LOG_FILENAME = "logging/logged_data.csv"

class Agent:
    def __init__(self, username, password, prior_obj):
        self.username = username
        # Initialize the Speakeasy Python framework and login.
        self.speakeasy = Speakeasy(host=DEFAULT_HOST_URL, username=username, password=password)
        self.speakeasy.login()  # This framework will help you log out automatically when the program terminates.
        self.prior_obj = prior_obj

    def listen(self):
        while True:
            # only check active chatrooms (i.e., remaining_time > 0) if active=True.
            rooms: List[Chatroom] = self.speakeasy.get_rooms(active=True)
            for room in rooms:
                if not room.initiated:
                    # send a welcome message if room is not initiated
                    room.post_messages(f'Hello! This is mr_ripley_{room.my_alias}. I am a masters student in Film Studies. Feel free to ask me movie related questions :)')
                    room.initiated = True
                # Retrieve messages from this chat room.
                # If only_partner=True, it filters out messages sent by the current bot.
                # If only_new=True, it filters out messages that have already been marked as processed.
                for message in room.get_messages(only_partner=True, only_new=True):
                    msg_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    print(
                        f"\t- Chatroom {room.room_id} "
                        f"- new message #{message.ordinal}: '{message.message}' "
                        f"- {self.get_time()}")
                    try:
                        reply = getResponse(message.message, self.prior_obj)
                    except Exception as err:
                        print(err)
                        reply = DEFAULT_MSG
                    room.post_messages(reply)
                    reply_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    room.mark_as_processed(message)
                    log_to_csv(LOG_FILENAME, message.message, msg_time, reply, reply_time)

                
                # Retrieve reactions from this chat room.
                # Not using at this moment.
                # If only_new=True, it filters out reactions that have already been marked as processed.
                for reaction in room.get_reactions(only_new=True):
                    print(
                        f"\t- Chatroom {room.room_id} "
                        f"- new reaction #{reaction.message_ordinal}: '{reaction.type}' "
                        f"- {self.get_time()}")
                    # Implement your agent here #
                    room.post_messages(f"Received your reaction: '{reaction.type}' ")
                    room.mark_as_processed(reaction)  
            time.sleep(listen_freq)

    @staticmethod
    def get_time():
        return time.strftime("%H:%M:%S, %d-%m-%Y", time.localtime())


if __name__ == '__main__':
    prior_obj = Preprocess()
    demo_bot = Agent("swelter-animato-kitchen_bot", "sLGLWSn0901EVg", prior_obj)
    demo_bot.listen()
