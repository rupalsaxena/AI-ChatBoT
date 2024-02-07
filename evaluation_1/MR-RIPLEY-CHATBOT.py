from speakeasypy import Speakeasy, Chatroom
from typing import List
import time
import utils

DEFAULT_HOST_URL = 'https://speakeasy.ifi.uzh.ch'
listen_freq = 2


class Agent:
    def __init__(self, username, password):
        self.username = username
        # Initialize the Speakeasy Python framework and login.
        self.speakeasy = Speakeasy(host=DEFAULT_HOST_URL, username=username, password=password)
        self.speakeasy.login()  # This framework will help you log out automatically when the program terminates.
        self.graph = utils.load_graphs()

    def listen(self):
        while True:
            # only check active chatrooms (i.e., remaining_time > 0) if active=True.
            rooms: List[Chatroom] = self.speakeasy.get_rooms(active=True)
            for room in rooms:
                if not room.initiated:
                    # send a welcome message if room is not initiated
                    room.post_messages(f'Hello! This is mr_ripley_ \n\n{room.my_alias}. Please input a SPARQL Query.')
                    room.initiated = True
                # Retrieve messages from this chat room.
                # If only_partner=True, it filters out messages sent by the current bot.
                # If only_new=True, it filters out messages that have already been marked as processed.
                for message in room.get_messages(only_partner=True, only_new=True):
                    print(
                        f"\t- Chatroom {room.room_id} "
                        f"- new message #{message.ordinal}: '{message.message}' "
                        f"- {self.get_time()}")

                    # Implement your agent here #
                    # Logic for 1st evaluation.
                    msg = str(message.message)
                    q_type = "SPARQL" #utils.check_q_type(msg) # Check the type of question for further scailability.

                    if q_type == "SPARQL":
                        #sparql = utils.sparql_parser(msg) # Added to clean the request and retrive only SPARQL statement.
                        try:
                            responses = self.graph.query(msg)
                            responses_list = [utils.remove_special_characters(str(result)) for result, in responses]
                            print(responses_list)

                            post_messages = f"Here is the information you are looking for. {responses_list}"
                            room.post_messages(post_messages)

                        except Exception as error:
                            print(error)
                            post_messages = f"Hmm... I am in a fog. Please send a valid SPARQL query! {error}"
                            room.post_messages(post_messages)
                    
                    else:
                        post_messages = '''Sorry... I couldn't recognize what you are asking.
                        I am really good at finding information based on SPARQL though.
                        How about giving me a question in a SPARQL format like:
                        PREFIX ... SELECT ... ...'''
                        room.post_messages(post_messages)
                    
                    # Set this message in this room as a processed one.
                    # To prevent duplicate tasks.
                    room.mark_as_processed(message)

                """
                Retrieve reactions from this chat room.
                Not using at this moment.
                If only_new=True, it filters out reactions that have already been marked as processed.
                for reaction in room.get_reactions(only_new=True):
                    print(
                        f"\t- Chatroom {room.room_id} "
                        f"- new reaction #{reaction.message_ordinal}: '{reaction.type}' "
                        f"- {self.get_time()}")
                    # Implement your agent here #
                    room.post_messages(f"Received your reaction: '{reaction.type}' ")
                    room.mark_as_processed(reaction)
                """
                
            time.sleep(listen_freq)

    @staticmethod
    def get_time():
        return time.strftime("%H:%M:%S, %d-%m-%Y", time.localtime())


if __name__ == '__main__':
    demo_bot = Agent("username", "password")
    demo_bot.listen()
