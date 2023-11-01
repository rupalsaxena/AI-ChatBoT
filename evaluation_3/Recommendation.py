import random
from Levenshtein import distance
from EntityRecognition import EntityRecognition

DEFAULT_RESPONSES = [
    "I don't find any suitable recommendation for you! Do you want me to look for something else?",
    "I don't find any recommendation for you. Can I help you with something else?",
    "I am not sure I understand it properly. Try to rephrase it.",
]

# TODO: handle genre recommendation serperately 
# TODO: movies for humans

class Recommend:
    def __init__(self, msg, graph, prior_obj):
        self.msg = msg
        self.graph = graph
        self.prior_obj = prior_obj
        self.embed = self.prior_obj.get_emb_obj()
        self.responses = []
        self.ent_dict = self.recognize_entities()
        if len(self.ent_dict) > 0:
            self.process()
        self.chooseResponse()
    
    def process(self):
        for label in self.ent_dict:
            if self.ent_dict[label]["tag"] == "ACTOR":
                recos = self.graph.queryActor(self.ent_dict[label]["id"])
            elif self.ent_dict[label]["tag"] == "GENRE":
                recos = self.graph.queryMoviesfromGenres(self.ent_dict[label]["id"])
            else:
                recos = self.embed.find_similar_entities(self.ent_dict[label]["id"])
            self.responses.extend(recos)

    def recognize_entities(self):
        er = EntityRecognition(self.msg, prior_obj=self.prior_obj)
        ent_dict = er.process()
        return ent_dict

    def chooseResponse(self):
        if len(self.responses) > 1:
            if len(self.responses) > 6:
                random.shuffle(self.responses)
                self.responses = self.responses[0:5]
            init_resp = "Here are some recommendations:"
            response=""
            for i, resp in enumerate(self.responses):
                if i == 0:
                    response = response + " " + resp 
                else:
                    response = response + ", " + resp 
            response = init_resp + response 
        elif len(self.responses) == 0:
            response = random.choice(DEFAULT_RESPONSES)
        elif len(self.responses) == 1:
            response = self.responses[0]
            response = "I think it is "+response + "."
        self._response = response

    def getResponse(self):
        return self._response