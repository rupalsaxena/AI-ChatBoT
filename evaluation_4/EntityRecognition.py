import difflib
from flair.data import Sentence
from Constants import SPECIAL_CHARS

manual_fix = {"Weathering with You": "Q59692464"}

class EntityRecognition:
    def __init__(self, input, prior_obj=None):
        self.input = input
        self.prior_obj = prior_obj
        self.ner = prior_obj.getNERModel()
        self.emb = prior_obj.get_emb_obj()
        for char in SPECIAL_CHARS:
            self.input = self.input.replace(char, "")
    
    def process(self):
        self.ent_dict = self.recog_ent_label()
        self.clean_ent_labels()
        
        for label in self.ent_dict:
            for key in manual_fix:
                if label in key:
                    id = manual_fix[key]
                else:
                    id = -1
            if id == -1:
                id = self.emb.getIDfromLabel(label)
                if id == -1:
                    id = self.get_id_from_loaded_data(label)
            self.ent_dict[label]["id"] = id
        print(self.ent_dict)
        return self.ent_dict
    
    def clean_ent_labels(self):
        new_dict = self.ent_dict.copy()
        for label in self.ent_dict:
            if "box office" in label:
                new_label = label.replace("box office", "")
                new_dict[new_label] = new_dict.pop(label)
            if "," in label:
                entities = label.split(",")
                for entity in entities:
                    new_dict[entity] = {}
                    new_dict[entity]["tag"] = self.ent_dict[label]["tag"]
        self.ent_dict = new_dict.copy()

    def recog_ent_label(self):
        flair_input = Sentence(self.input)
        self.ner.predict(flair_input)
        prediction = flair_input.get_spans('ner')
        tags = {}
        for entity in prediction:
            tags[entity.text] = {}
            tags[entity.text]["tag"] = entity.tag
        return tags
    
    def match_id(self, label, df, cutoff=0.6):
        id = -1
        df['names'] = df['names'].apply(lambda x: x.strip())
        closest_matches = difflib.get_close_matches(label, df['names'].tolist(), cutoff=cutoff)
        if len(closest_matches)>0:
            closest_match = closest_matches[0]
            id = df['ids'][df['names']==closest_match].tolist()
            return id[0]
        return id

    def get_id_from_loaded_data(self, label):
        id = -1
        if self.ent_dict[label]["tag"] == "RATING":
            return id
        # if self.ent_dict[label]["tag"] == "TITLE":
        #     print("search in movies")
        #     movies_df = self.prior_obj.getMovies()
        #     id = self.match_id(label.lower(), movies_df)
        #     if id == -1:
        #         id = self.match_id(label.lower(), movies_df, cutoff=0.4)
        if self.ent_dict[label]["tag"] == "ACTOR":
            print("search in humans")
            human_df = self.prior_obj.getHumans()
            id = self.match_id(label.lower(), human_df)
            if id == -1:
                id = self.match_id(label.lower(), human_df, cutoff=0.4)
        elif self.ent_dict[label]["tag"] == "GENRE":
            print("search in genres")
            genre_df = self.prior_obj.getGenre()
            id = self.match_id(label.lower(), genre_df)
            if id == -1:
                id = self.match_id(label.lower(), genre_df, cutoff=0.4)
        elif self.ent_dict[label]["tag"] == "CHARACTER":
            print("searching in characters")
            char_df = self.prior_obj.getChars()
            id = self.match_id(label.lower(), char_df)
            if id == -1:
                id = self.match_id(label.lower(), char_df, cutoff=0.4)
        else:
            print("searching in full list")
            all_df = self.prior_obj.getAllEntities()
            id = self.match_id(label.lower(), all_df)
            if id == -1:
                id = self.match_id(label.lower(), all_df, cutoff=0.4)
        return id
