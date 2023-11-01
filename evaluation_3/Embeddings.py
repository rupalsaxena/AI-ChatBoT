import csv
import numpy as np
import os
import random
import rdflib
import pandas as pd
from sklearn.metrics import pairwise_distances

WD = rdflib.Namespace('http://www.wikidata.org/entity/')
WDT = rdflib.Namespace('http://www.wikidata.org/prop/direct/')
DDIS = rdflib.Namespace('http://ddis.ch/atai/')
RDFS = rdflib.namespace.RDFS
SCHEMA = rdflib.Namespace('http://schema.org/')

class Embeddings:
    def __init__(self, graph):
        self.graph = graph
        self.load_embeddings()
        self.load_emb_dict()

    def load_embeddings(self):
        # load the embeddings
        print("loading embeddings")
        self.entity_emb = np.load('data/entity_embeds.npy')
        self.relation_emb = np.load('data/relation_embeds.npy')
    
    def load_emb_dict(self):
        print("loading embedding dicts")
        with open('data/entity_ids.del', 'r') as ifile:
            self.ent2id = {rdflib.term.URIRef(ent): int(idx) for idx, ent in csv.reader(ifile, delimiter='\t')}
            self.id2ent = {v: k for k, v in self.ent2id.items()}
        with open('data/relation_ids.del', 'r') as ifile:
            self.rel2id = {rdflib.term.URIRef(rel): int(idx) for idx, rel in csv.reader(ifile, delimiter='\t')}
            self.id2rel = {v: k for k, v in self.rel2id.items()}
        self.ent2lbl = {ent: str(lbl) for ent, lbl in self.graph.subject_objects(RDFS.label)}
        self.lbl2ent = {lbl: ent for ent, lbl in self.ent2lbl.items()}
    
    def apply_embedding(self, ent_id, pred_id):
        try:
            head = self.entity_emb[self.ent2id[WD[ent_id]]]
            pred = self.relation_emb[self.rel2id[WDT[pred_id]]]
            lhs = head + pred
            dist = pairwise_distances(lhs.reshape(1, -1), self.entity_emb).reshape(-1)
            most_likely = dist.argsort()
            df = pd.DataFrame([(self.id2ent[idx][len(WD):], self.ent2lbl[self.id2ent[idx]], dist[idx], rank+1) for rank, idx in enumerate(most_likely[:4])], columns=('Entity', 'Label', 'Score', 'Rank'))
            print(df)
            return [df["Label"].values[0], df["Label"].values[1], df["Label"].values[2]]
        except:
            print("embedings failing")
            return [-1, -1]
    
    def find_similar_entities(self, id):
        try:
            ent = self.ent2id[WD[id]]
            dist = pairwise_distances(self.entity_emb[ent].reshape(1, -1), self.entity_emb).reshape(-1)
            most_likely = dist.argsort()
            most_likely = most_likely[1:10]
            random.shuffle(most_likely)
            most_likely = most_likely[0:5]

            df = pd.DataFrame([
                (
                    self.id2ent[idx][len(WD):], # qid
                    self.ent2lbl[self.id2ent[idx]],  # label
                    dist[idx],             # score
                    rank+1,                # rank
                )
                for rank, idx in enumerate(most_likely)],
                columns=('Entity', 'Label', 'Score', 'Rank'))
            return df['Label'].values
        except:
            print("embeddings did not find anything")
            return []

    def getEntityEmb(self):
        return self.entity_emb
    
    def getRelationEmb(self):
        return self.relation_emb
    
    def getIDfromLabel(self, label):
        try:
            ent =  str(self.lbl2ent[label]).split("/")[-1]
        except:
            ent =  -1
        return ent
