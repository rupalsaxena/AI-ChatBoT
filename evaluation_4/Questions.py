import random
from EntityRecognition import EntityRecognition
from PredicateRecognition import RecognizePredicate

DEFAULT_RESPONSES = [
    "Umm! I don't think I understand that! Can I help you in some other way?",
    "Hmmmmm! I am not sure what you mean. Can you rephrase it or ask another question?",
    "Honestly, I don't know this. :P",
    "I don't have an answer for this. Can I help you with something else?"
]

class Question:
    def __init__(self, msg, prior_obj, graph):
        self.msg = msg
        self.prior_obj = prior_obj
        self.graph = graph
        self.responses = []
        self.embed = self.prior_obj.get_emb_obj()
        ent_dict = self.recognize_entities()
        preds, pred_ids = self.recognize_predicate(ent_dict)
        print("predicate:", preds, pred_ids)
        if len(ent_dict)>0 and len(pred_ids)>0:
            self.process(ent_dict, pred_ids)
        self.chooseResponse()

    def process(self, ent_dict, pred_ids):
        # factual query
        self.fact_resp = []
        for label in ent_dict:
            ent_id = ent_dict[label]["id"]
            if ent_id != -1:
                for pred_id in pred_ids:
                    if pred_id == "P577":
                        response = self.graph.queryMovieReleaseDates(ent_id)
                    else:  
                        response = self.graph.queryFactual(ent_id, pred_id)
                    self.fact_resp.extend(response)
        
        # embedding query
        self.emb_resp = []
        self.from_embedding = False
        if len(self.fact_resp) < 1:
            for label in ent_dict:
                for pred_id in pred_ids:
                    response = self.embed.apply_embedding(ent_dict[label]["id"], pred_id)
                    if response[0] != -1:
                        self.emb_resp.append(response)
            if len(self.emb_resp) > 0:
                self.from_embedding=True
                if len(self.emb_resp) == 1:
                    self.responses = self.emb_resp[0]
                else:
                    self.responses = random.choice(self.emb_resp)
        else:
            self.responses = self.fact_resp
        print("responses:", self.responses)

    def recognize_entities(self):
        er = EntityRecognition(self.msg, prior_obj=self.prior_obj)
        ent_dict = er.process()
        return ent_dict
    
    def recognize_predicate(self, ent_dict):
        # remove entities from predicates
        msg = self.msg
        for label in ent_dict:
            # if entity name is more than one word then remove all words from msg
            ent_words = label.split(" ")
            id = ent_dict[label]["id"]
            if id != -1:
                # replace all entities from main msg
                for ent_word in ent_words:
                    msg = msg.replace(ent_word, "")

        # recognize predicates
        all_preds = self.prior_obj.get_all_predicates()
        rp = RecognizePredicate(msg, prior=all_preds)
        preds, pred_ids = rp.get_predicate_ID()
        return preds, pred_ids

    def chooseResponse(self):
        if len(self.responses) > 1:
            if self.from_embedding:
                core = "According to embeddings, your answers are"
            else:
                core = "I think it's "
            for i, response in enumerate(self.responses):
                if i == 0:
                    core = core + " " + response
                else:
                    core = core + ", " + response
            response = core
        elif len(self.responses) == 0:
            response = random.choice(DEFAULT_RESPONSES)
        elif len(self.responses) == 1:
            response = self.responses[0]
            if self.from_embedding:
                response = "The answer suggested by embedding is: " + response + "."
            else:
                response = "I think it is " + response + "."
        self._response = response

    def getResponse(self):
        return self._response
