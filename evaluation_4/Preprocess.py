import os
import json
import pandas as pd
import Constants
from nltk.corpus import stopwords
from flair.models import SequenceTagger
from Graphs import Graphs
from QuestionRecognition import QuestionRecognition
from Embeddings import Embeddings
from Crowdsourcing import Crowdsourcing

class Preprocess:
    def __init__(self):
        self.datapath="data"
        self.load_all_entities()
        self.load_predicates()
        self.load_default_data()
        self.load_NER_model()
        self.load_images()
        self.question_model = QuestionRecognition()
        self.crowd_obj = Crowdsourcing(self.all_entities)
        self.g = Graphs()
        self.embed_obj = Embeddings(self.g.get_graph())
        
    def load_NER_model(self):
        print("loading NER model")
        self.ner_model = SequenceTagger.load("models/ner.pt")
    
    def load_default_data(self):
        foldername = "data/all_data_folder"

        print("loading humans data")
        self.humans = pd.read_csv(os.path.join(foldername, "all_humans.csv"))
        self.humans["names"] = self.humans["names"].apply(lambda x: x.lower())
        self.humans["ids"] = self.humans["ids"].apply(lambda x: x.split("/")[-1])

        print("loading movies data")
        self.movies = pd.read_csv(os.path.join(foldername, "all_movies.csv"))
        self.movies["names"] = self.movies["names"].apply(lambda x: x.lower())
        self.movies["ids"] = self.movies["ids"].apply(lambda x: x.split("/")[-1])

        print("loading character data")
        self.chars = pd.read_csv(os.path.join(foldername, "all_character.csv"))
        self.chars["names"] = self.chars["names"].apply(lambda x: x.lower())
        self.chars["ids"] = self.chars["ids"].apply(lambda x: x.split("/")[-1])

        print("loading genres data")
        self.genre = pd.read_csv(os.path.join(foldername, "all_genres.csv"))
        self.genre["names"] = self.genre["names"].apply(lambda x: x.lower())
        self.genre["ids"] = self.genre["ids"].apply(lambda x: x.split("/")[-1])

        print("loading awards data")
        self.awards = pd.read_csv(os.path.join(foldername, "all_awards.csv"))
        self.awards["names"] = self.awards["names"].apply(lambda x: x.lower())
        self.awards["ids"] = self.awards["ids"].apply(lambda x: x.split("/")[-1])

    def load_all_entities(self):
        foldername = "data/"
        print("loading all entity data")
        self.all_entities = pd.read_csv(os.path.join(foldername, "entity_mappings.csv"))
        self.all_entities = self.all_entities.astype(str)
        self.all_entities["label"] = self.all_entities["label"].apply(lambda x: x.lower())
        self.all_entities.rename(columns = {'label':'names'}, inplace = True)
        self.all_entities.rename(columns = {'wiki_code':'ids'}, inplace = True)
        self.all_entities.drop(columns='description', inplace=True)
    
    def load_images(self):
        path = "data/images.json"
        f = open(path)
        self.images = json.load(f)
    
    def getImages(self):
        return self.images

    def getAllEntities(self):
        return self.all_entities

    def getHumans(self):
        return self.humans
    
    def getMovies(self):
        return self.movies
    
    def getGenre(self):
        return self.genre
    
    def getChars(self):
        return self.chars
    
    def getAwards(self):
        return self.awards

    def getDefaultData(self):
        return self.humans, self.movies, self.chars, self.genre, self.awards
    
    def getNERModel(self):
        return self.ner_model

    def load_predicates(self):
        print("loading all predicates")
        self.df_pred = pd.read_csv("data/all_predicates.csv")
        self.df_pred['predicate'] = self.df_pred['predicate'].apply(lambda x: str(x))
    
    def get_all_predicates(self):
        return self.df_pred
    
    def get_graph(self):
        return self.g
    
    def get_emb_obj(self):
        return self.embed_obj
    
    def get_question_model(self):
        return self.question_model
    
    def remove_stopwords(self, input):
        # removing stopwords and useless words from input
        words = input.split(" ")
        stop_words = stopwords.words('english')
        stop_words.extend(Constants.USELESS_WORDS)

        filtered_input = []
        for word in words:
            for char in Constants.SPECIAL_CHARS:
                if char in word:
                    word = word.replace(char, "")
            if word not in stop_words:
                filtered_input.append(word)
        return filtered_input

    def get_crowd_obj(self):
        return self.crowd_obj

if __name__=="__main__":
    p = Preprocess()