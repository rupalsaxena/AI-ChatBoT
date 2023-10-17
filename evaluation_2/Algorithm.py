import random
from Questions import Question

GREETINGS = [
    "Good luck with Evaluation today :) I am sure you are enjoying this :)",
    "I hope you are having a nice day :)",
    "Best wishes for you :D",
    "Good Luck :D",
    "Enjoy :D",
]
help_str = "Hello, I am MR. Ripley. \n I can answer following types of questions, examples attached with each type of question: \n FACTUAL QUESTIONS: Who is director of The Bridge on the River Kwai? \n EMBEDDING QUESTIONS: Who is screenwriter of The Masked Gang: Cyprus? \n  MULTIMEDIA QUESTIONS: Show me a picture of Halle Berry. \n RECOMMENDATION QUESTIONS: Recommend movies similar to Hamlet and Othello. \n I hope you enjoy playing with me :)"

def getResponse(msg, prior_obj):
    print(msg)
    alg = Algorithm(msg, prior_obj)
    response = alg.get_reply()
    print("response:", response)
    return response

class Algorithm:
    def __init__(self, input, prior_obj):
        self.input = input
        self.greeting()
        self.help()
        if not self.is_help:
            if  not self.is_greeting: 
                self.prior_obj = prior_obj
                # load graph
                self.graph = self.prior_obj.get_graph()
                # look for answer from question
                self.reply = self.question()
            else:
                self.reply = random.choice(GREETINGS)
        else:
            self.reply = help_str

    def question(self):
        qe = Question(self.input, self.prior_obj, self.graph)
        response = qe.getResponse()
        return response

    def greeting(self):
        list = self.input.split(" ")
        if len(list) < 3:
            self.is_greeting = True
        else:
            self.is_greeting = False
    
    def help(self):
        if self.input.lower() == "help":
            self.is_help = True
        else:
            self.is_help = False

    def get_reply(self):
        return self.reply
