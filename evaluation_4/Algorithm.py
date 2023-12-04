import random
from Questions import Question
from Multimedia import Multimedia
from Recommendation import Recommend

GREETINGS = [
    "Good luck with Evaluation today :) I am sure you are enjoying this :)",
    "I hope you are having a nice day :)",
    "Best wishes for you :D",
    "Good Luck :D",
    "Enjoy :D",
]

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

        if  not self.is_greeting: 
            self.prior_obj = prior_obj

            # load graph
            self.graph = self.prior_obj.get_graph()

            # question detection
            question_model = self.prior_obj.get_question_model()
            category = question_model.get_question_category(input.lower())
            print(f"Question Category : {category}")
            if category != -1:
                # process each type of question
                if category == "multimedia":
                    self.reply = self.multimedia()
                elif category == "recommendation":
                    self.reply = self.recommend()
                else:
                    self.reply = self.question()
        else:
            self.reply = random.choice(GREETINGS)

    def multimedia(self):
        mm = Multimedia(self.input, self.graph, self.prior_obj)
        response = mm.getResponse()
        return response
    
    def recommend(self):
        re = Recommend(self.input, self.graph, self.prior_obj)
        response = re.getResponse()
        return response

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

    def get_reply(self):
        return self.reply