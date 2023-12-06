import random
from Levenshtein import distance
from EntityRecognition import EntityRecognition
from PredicateRecognition import RecognizePredicate

DEFAULT_RESPONSES = [
    "I don't find any suitable recommendation for you! Do you want me to look for something else?",
    "I don't find any recommendation for you. Can I help you with something else?",
    "I am not sure I understand it properly. Try to rephrase it.",
]

class Recommend:
    def __init__(self, msg, graph, prior_obj):
        self.msg = msg
        self.graph = graph
        self.prior_obj = prior_obj
        self.embed = self.prior_obj.get_emb_obj()
        self.responses = []
        self.ent_dict = self.recognize_entities()
        self.preds, self.pred_ids = self.recognize_predicate(self.ent_dict)
        print("predicate:", self.preds, self.pred_ids)
        if len(self.ent_dict)>0:
            self.process()
        self.chooseResponse()

    def process(self):
        if len(self.pred_ids) > 0:
            for label in self.ent_dict:
                self.emb_resp = []
                for pred_id in self.pred_ids:
                    recos_emb = self.embed.apply_embedding(self.ent_dict[label]["id"], pred_id)
                    if recos_emb[0] != -1:
                        self.emb_resp.extend(recos_emb)
                self.responses.extend(self.emb_resp)

                if len(self.responses) < 1:
                    self.get_reco_from_ent()
        else:
            self.get_reco_from_ent()
        self.remove_entity_from_response()

    def remove_entity_from_response(self):
        for ent in self.ent_dict:
            if ent in self.responses:
                self.responses.remove(ent)

    def get_reco_from_ent(self):
        for label in self.ent_dict:
            if self.ent_dict[label]["tag"] == "ACTOR":
                recos = self.graph.queryActor(self.ent_dict[label]["id"])
            elif self.ent_dict[label]["tag"] == "DIRECTOR":
                recos = self.graph.queryMoviesfromDirector(self.ent_dict[label]["id"])
            elif self.ent_dict[label]["tag"] == "GENRE":
                recos = self.graph.queryMoviesfromGenres(self.ent_dict[label]["id"])
            else:
                recos = self.embed.find_similar_entities(self.ent_dict[label]["id"])
            self.responses.extend(recos)
    
    def recognize_entities(self):
        er = EntityRecognition(self.msg, prior_obj=self.prior_obj)
        ent_dict = er.process()
        return ent_dict

    def recognize_predicate(self, ent_dict):
        # recognize predicates
        all_preds = self.prior_obj.get_all_predicates()
        rp = RecognizePredicate(self.msg, prior=all_preds)
        preds, pred_ids = rp.get_predicate_ID()
        return preds, pred_ids

    def chooseResponse(self):
        if len(self.responses) > 1:
            if len(self.responses) > 6:
                random.shuffle(self.responses)
                self.responses = self.responses[0:5]
            init_resp = "Here are some recommendations for you: \n"
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