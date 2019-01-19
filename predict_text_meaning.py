# -*- coding: utf-8 -*-
#By abin and hari

from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
import pandas as pd
import os
from keras.models import model_from_json
import nltk
EMBEDDING_FILE='glove/wiki.ml.vec'#glove.6B.300d.txt'
TRAIN_FILE='data/querydata(m)f.tsv'
VOC_FILE='word_map_ml.json'
MODEL_FILE="model_ml.json"
MODEL_WEIGHT="model_ml.h5"
MODEL_PIC='model_ml.png'
SUGGEST_DATA='data/querydata_to_be_suggested(m)f.tsv'

os.environ['KERAS_BACKEND'] = 'theano'


def load_map():
    import json
    with open(VOC_FILE, 'r',encoding='utf-8') as fp:
        word_map = json.load(fp)
    #print(word_map)
    return word_map
def load_model():
    json_file = open(MODEL_FILE, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    model = model_from_json(loaded_model_json)
    # load weights into new model
    model.load_weights(MODEL_WEIGHT)
    print("Loaded model from disk")
    return model
def load_data():
    data_train = pd.read_csv(SUGGEST_DATA, sep='\t',encoding='utf-8')
    return data_train
def predict(text,model,word_map,data_train):

    if(len(text[0])>0):
        print(text)

        t = Tokenizer()
        t.fit_on_texts(text)
        #print(text)
        tok_docs = []





        tok = nltk.word_tokenize(text[0])
        tok_docs.append(tok)
        #print(tok_docs)
        # word_map=load_map()
        max1=max(word_map.values())
        text_seq=[]
        for sent in tok_docs:
            s1=[]
            for w in sent:
                if w in word_map.keys():
                    s1.append(word_map[w])
                # else:
                #     #max1=max1+1
                #     s1.append(0)

            text_seq.append(s1)
        #print(text_seq)
        max_length = 50
        padded_docs = pad_sequences(text_seq, maxlen=max_length, padding='post')


        pred = model.predict(padded_docs)

        # print(pred)
        # print(padded_docs)
        out = []
        print(pred)
        for doc in pred:
            out.append(doc.tolist().index(max(doc.tolist())))
        print(out)

        if(pred.tolist()[0][out[0]]>0.85):
            print(pred.tolist()[0][out[0]])
            return (data_train.loc[data_train['sentiment'] == out[0]]['question']).values.tolist()[0]
        else:
            print(pred.tolist()[0][0])
            return (data_train.loc[data_train['sentiment'] == 0]['question']).values.tolist()[0]
    else:

        return ""

# l=predict(["ഹോട്ടലുകളുടെ "])
# print(l)
# print(predict(['ഹോട്ടലുകളുടെ പട്ടിക തരുക']))