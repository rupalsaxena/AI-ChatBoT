import os 
from typing import List
from flair.data import Sentence
from flair.data import Corpus
from flair.models import SequenceTagger
from flair.trainers import ModelTrainer
from flair.datasets import ColumnCorpus 
from flair.embeddings import WordEmbeddings, StackedEmbeddings
from flair.embeddings.base import TokenEmbeddings

TRAIN_DATA_PATH = 'train.txt'
TEST_DATA_PATH = 'test.txt'
DEV_DATA_PATH = 'dev.txt'
DATA_FOLDER = 'data/'
FINAL_MODEL_PATH = 'model/ner'

def train_model():
    columns = {0:'ner', 1:'text'}
    corpus: Corpus = ColumnCorpus(DATA_FOLDER, columns, train_file = TRAIN_DATA_PATH, test_file = TEST_DATA_PATH, dev_file = DEV_DATA_PATH)
    label_type = 'ner'
    tag_dictionary = corpus.make_label_dictionary(label_type=label_type)
    embedding_types : List[TokenEmbeddings] = [WordEmbeddings('glove')]
    embeddings : StackedEmbeddings = StackedEmbeddings(embeddings=embedding_types)
    tagger : SequenceTagger = SequenceTagger(hidden_size=256,
                                    embeddings=embeddings,
                                    tag_dictionary=tag_dictionary,
                                    tag_type=label_type,
                                    use_crf=True)
    trainer : ModelTrainer = ModelTrainer(tagger, corpus)
    trainer.train(FINAL_MODEL_PATH,learning_rate=0.05,mini_batch_size=32,max_epochs=50)

def test_model():
    model = SequenceTagger.load(os.path.join(FINAL_MODEL_PATH, 'ner.pt'))
    sentence = Sentence('Recommend me some movies of Priyanka Chopra')
    model.predict(sentence)
    print(sentence.to_tagged_string())
    
if __name__=="__main__":
    train_model()
    test_model()
