import csv
import numpy as np
import os
import random
import rdflib
import pandas as pd
from sklearn.metrics import pairwise_distances
import copy

# TODO:
# load_crowd_ans_data.csv
# answer_from_crowd:
#   input: ent_id, pred_id
#   output: label, votinginfo, inter-rater score



class Crowdsourcing:
    def __init__(self, all_entities):
        self.load_crowdsource_data()
        self.all_entities = all_entities

    def load_crowdsource_data(self):
        # load a processed crowdsource data
        print("loading a processed crowdsource data")
        self.df_crowd = pd.read_json('./data/crowd_data_processed.json')

    def search_from_crowdsource(self, ent_id, pred_id):

        df = self.df_crowd.copy()

        # Query answer from crowdsource data
        search = (df['Input1ID']==ent_id)&(df['Input2ID']==pred_id)
        if sum(search) == 0:
            print("No crowdsourcing data!")
            return None, None
        # Get answer
        data = df.loc[search]
        res = data['Input3ID'].to_list()[0]
        info = copy.deepcopy(data.iloc[0][['SCORE', 'CORRECT', 'INCORRECT', 'FIXING']].to_dict())
        # Change the answer if it has a fixed value
        if (info['CORRECT']<info['INCORRECT']) and (len(info['FIXING'].keys())!=0):
            if (info['FIXING']['item']=='Object'):
                old = res
                res = info['FIXING']['fixval']
                new = res
                print(f"Reponse corrected by crowd! from {old} to {new}")
        # Change entity id to label
        res_label = self.entid2label(res)
        info_fix = info['FIXING']
        if info_fix != {}:
            info_fix['fixval'] = self.entid2label(info_fix['fixval'])
            info['FIXING'] = info_fix

        if res_label == None:
            print(f"No crowdsourcing data! - New Entity ID {res}")

        print(f"Found crowdsourcing! {res_label}({res}) {info}")
        return res_label, info
    
    def entid2label(self, entity_id):
        # print(entity_id)
        if str(entity_id)[0] == 'Q':
            search = (self.all_entities['ids'] == entity_id)
            if sum(search) == 0:
                return None
            label = self.all_entities.loc[search]['names'].values[0]
            return label 
        return entity_id

