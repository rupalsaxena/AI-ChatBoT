import random
from EntityRecognition import EntityRecognition

DEFAULT_RESPONSE = [
    "I am sorry but I don't find any suitable results for you.",
    "I don't have any results for this.",
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
        self.query_results = []

        for label in ent_dict:
            id = ent_dict[label]["id"]
            if id != -1:
                self.query_results.extend(self.graph.queryMultimedia2(id))
            else:
                print("querry multimedia using label")
        
        id = self.chooseQueryRes()
        if id != -1:
            img = self.id2img(id)
        else:
            img = random.choice(DEFAULT_RESPONSE)

        if img == -1:
            self._response = random.choice(DEFAULT_RESPONSE)
        else:
            self._response = img


    def id2img(self, id):
        group_imgs=[]
        img = -1
        for dict in self.images:
            if id in dict["cast"]:
                if len(dict["cast"]) == 1:
                    img = dict["img"]
                    break
                else:
                    group_imgs.append(dict)
        print(group_imgs)
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
            response = random.choice(self.query_results)
        elif len(self.query_results) == 0:
            response = -1
        elif len(self.query_results) == 1:
            response = self.query_results[0]
        return response
    
    def getResponse(self):
        return self._response
