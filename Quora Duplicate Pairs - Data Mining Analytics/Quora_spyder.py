

import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import stopwords
from difflib import SequenceMatcher
from nltk.stem import SnowballStemmer
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

from tqdm import tqdm
import gensim
import tensorflow
import keras

#functions
def remove_stopwords(text):
    operators= set(('and','or','not','is','for'))
    stops = set(stopwords.words("english"))-operators
    return [w for w in text if not w in stops]

def concatenate_tokens(token_list):
    return str(' '.join(token_list))

def find_similarity(sent1, sent2):
	return SequenceMatcher(lambda x: x in (' ', '?', '.', '""', '!'), sent1, sent2).ratio()

def return_common_tokens(sent1, sent2):
    return " ".join([word.lower() for word in sent1 if word in sent2])

          
       



#read files
Train_rawdata = pd.read_csv('D:/vaibhav/DataMining/Project/train.csv',encoding="utf-8",nrows=10000)
Test_rawdata = pd.read_csv('D:/vaibhav/DataMining/Project/test.csv',encoding="utf-8",nrows=10000)


#removing questions with words less than 10
Train_rawdata.dtypes
Train_rawdata['question1'] = Train_rawdata['question1'].astype('str')
Train_rawdata['question2'] = Train_rawdata['question2'].astype('str')
Train_rawdata = Train_rawdata[Train_rawdata['question2'].map(len)>9]
Train_rawdata = Train_rawdata[Train_rawdata['question1'].map(len)>9]

Test_rawdata['question1'] = Test_rawdata['question1'].astype('str')
Test_rawdata['question2'] = Test_rawdata['question2'].astype('str')
Test_rawdata = Test_rawdata[Test_rawdata['question2'].map(len)>9]
Test_rawdata = Test_rawdata[Test_rawdata['question1'].map(len)>9]



# tokenize
#Train_questions_tokenized=Train_questions.apply(nltk.word_tokenize)
# tokenize
Train_questions = list(Train_rawdata['question1']) + list(Train_rawdata['question2'])
c = 0
for question in tqdm(Train_questions):
    Train_questions[c] = list(gensim.utils.tokenize(question, deacc=True, lower=True))
    c += 1
    
# train model
model = gensim.models.Word2Vec(Train_questions, size=300, workers=16, iter=10, negative=20)

# trim memory
model.init_sims(replace=True)

# creta a dict 
w2v = dict(zip(model.wv.index2word, model.wv.syn0))


v=pd.concat((Train_rawdata['question1'], Train_rawdata['question2'])).unique() 
tfidf = TfidfVectorizer(lowercase=False,)
tfidf.fit_transform(v)

# dict key:word and value:tf-idf score
word2tfidf = dict(zip(tfidf.get_feature_names(), tfidf.idf_))

#for key, value in w2v.items():
 #   print(key)
  #  print(value)
   # print(str(key))
    
    
#Deriving the naive features
for i in (1, 2):
        Train_rawdata['question%s_tokens' % i] = Train_rawdata['question%s' % i].apply(nltk.word_tokenize)
 
print(len(w2v))

#Deriving vectors
vecs1 = []

for qu in tqdm(list(Train_rawdata['question1_tokens'])):
    mean_vec = np.zeros([len(w2v), 300])
    for word in qu:
        vec = None
        tfidf_Val=None
        if word in w2v:
            vec=w2v[word]
        else:
            vec=np.zeros((1,300))
        #print(vec)
        if word in word2tfidf:
            tfidf_Val=word2tfidf[word]
        else:
            tfidf_Val=np.zeros((1,300))
       # print(tfidf_Val)
        mean_vec += vec * tfidf_Val
    
    mean_vec = mean_vec.mean(axis=0)
    vecs1.append(mean_vec)
Train_rawdata['q1_feats'] = list(vecs1)


vecs2 = []
for qu in tqdm(list(Train_rawdata['question2_tokens'])):
    mean_vec = np.zeros([len(w2v), 300])
    for word in qu:
        vec = None
        tfidf_Val=None
        if word in w2v:
            vec=w2v[word]
        else:
            vec=np.zeros((1,300))
        if word in word2tfidf:
            tfidf_Val=word2tfidf[word]
        else:
            tfidf_Val=np.zeros((1,300))
        mean_vec += vec * tfidf_Val
    
    mean_vec = mean_vec.mean(axis=0)
    vecs2.append(mean_vec)
Train_rawdata['q2_feats'] = list(vecs2)
print((np.array(Train_rawdata['q1_feats'])))
print(len(np.dot(np.array(Train_rawdata['q1_feats']),np.array(Train_rawdata['q2_feats']))))

print(Train_rawdata['q2_feats'][1])

cos=[]
dist=[]
for idx1 in range(len(Train_rawdata['q1_feats'])):
    print(idx1)
    print(Train_rawdata['q1_feats'][idx1])
    for idx2 in range(len(Train_rawdata['q2_feats'])):
        if idx1==idx2:
            cos.append(np.dot(np.array(Train_rawdata['q1_feats'][idx1]),np.array(Train_rawdata['q2_feats'][idx2]))/(np.sqrt(np.dot(np.array(Train_rawdata['q1_feats'][idx1]),np.array(Train_rawdata['q1_feats'][idx1]))) * np.sqrt(np.dot(np.array(Train_rawdata['q2_feats'][idx1]),np.array(Train_rawdata['q2_feats'][idx1])))))
            distances = (Train_rawdata['q2_feats'][idx1]-Train_rawdata['q1_feats'][idx1])**2
            distances = distances.sum(axis=-1)
            distances = np.sqrt(distances)
            dist.append(distances)
            
           # dist.append(np.linalg.norm(np.array(Train_rawdata['q2_feats'][idx1])-np.array(Train_rawdata['q1_feats'][idx1])))

Train_rawdata['cos'] = list(cos)
Train_rawdata['dist'] = list(dist)           
           # dist.append(np.square(np.array(Train_rawdata['q2_feats'][idx2])[:,None] - np.array(Train_rawdata['q1_feats'][idx1])).sum(axis=300).T)

Train_rawdata[np.isnan(Train_rawdata['cos'])] = np.median(Train_rawdata[~np.isnan(Train_rawdata['cos'])])

X=Train_rawdata[['cos','dist']] 
y = Train_rawdata['is_duplicate']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 111)

X_train[np.isnan(X_train)] = np.median(X_train[~np.isnan(X_train)])
#closingPriceTrain[np.isnan(closingPriceTrain)] = np.median(closingPriceTrain[~np.isnan(closingPriceTrain)])
#openingPriceTest[np.isnan(openingPriceTest)] = np.median(openingPriceTest[~np.isnan(openingPriceTest)])

#as response is 1 and 0 starting with logistic regression
model = LogisticRegression().fit(X_train, y_train)
prediction = pd.DataFrame(model.predict(X_test), columns = ['is_duplicate'], index = X_test.index)

trained_data=[]

trained_data[]


print(len(dist))

print(Train_rawdata['q1_feats'].shape)
print(Train_rawdata['q2_feats'].shape)









