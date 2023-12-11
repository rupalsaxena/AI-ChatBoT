import random
from EntityRecognition import EntityRecognition

DEFAULT_RESPONSE = [
    "I am sorry but I don't find any suitable results for you. Can I help you with something else?",
    "I don't have any results for this. Is there something else I can search for you?",
    "I looked into my dataset but unfortunately I did not find any results for this.",
    "I cannot find any results for you. Do you have any other question for me?"
]

class Multimedia:
    def __init__(self, input, graph, prior_obj):
        self.msg = input
        self.graph = graph
        self.prior_obj = prior_obj
        self.images = prior_obj.getImages()
        self.process()
    
    def process(self):
        er = EntityRecognition(self.msg, prior_obj=self.prior_obj)
        ent_dict = er.process()
        self.query_results = {}

        for label in ent_dict:
            id = ent_dict[label]["id"]
            if id != -1:
                response_ids = self.graph.queryMultimedia(id)
                for response_id in response_ids:
                    self.query_results[response_id] = ent_dict[label]["tag"]
            else:
                print("querry multimedia using label")
        
        id, type = self.chooseQueryRes()
        if id != -1 and type != -1:
            img = self.id2img(id, type)
        else:
            img = random.choice(DEFAULT_RESPONSE)

        if img == -1:
            self._response = random.choice(DEFAULT_RESPONSE)
        else:
            self._response = img


    def id2img(self, id, type):
        group_imgs=[]
        img = -1

        if type == "TITLE":
            search = "movie"
        else:
            search = "cast"

        for dict in self.images:
            if id in dict[search]:
                if len(dict[search]) == 1:
                    img = dict["img"]
                    break
                else:
                    group_imgs.append(dict)
        if img == -1:
            if len(group_imgs) > 0:
                img = random.choice(group_imgs)["img"]
        
        if img != -1:
            final_img = "image:" + img.split(".")[0]
            return final_img
        else:
            return -1

    def chooseQueryRes(self):
        if len(self.query_results) > 1:
            response, type = random.choice(list(self.query_results.items()))
        elif len(self.query_results) == 0:
            response = -1
            type = -1
        elif len(self.query_results) == 1:
            response  = next(iter(self.query_results))
            type = self.query_results[response]
        return response, type
    
    def getResponse(self):
        return self._response
