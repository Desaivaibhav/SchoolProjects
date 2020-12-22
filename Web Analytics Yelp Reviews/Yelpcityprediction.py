# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 18:12:28 2016

References:
https://github.com/wendykan/DeepLearningMovies/blob/master/BagOfWords.py #bag of words
https://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-1-for-beginners-bag-of-words
http://pandas-docs.github.io/pandas-docs-travis/basics.html #iterrows panda basics and row iteration
http://blog.rizauddin.com/2009/08/python-remove-items-from-list-that_2943.html #removing  elements of list from other list 
https://github.com/amueller/word_cloud # Word Cloud
http://scikit-learn.org/stable/modules/ensemble.html #feature-importance
https://www.dataquest.io/blog/machine-learning-python/ #train test split cross validation
"""



import pymongo
from pymongo import MongoClient
import os
import re
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from nltk.corpus import stopwords
from sklearn.metrics import accuracy_score
import pandas as pd
import numpy as np
from nltk.collocations import *
import wordcloud
from wordcloud import WordCloud
import matplotlib.pyplot as plt

print ("Start: "+time.strftime("%I:%M:%S")) 
client = MongoClient('localhost', 27017)
db = client.yelp #Database
#collections
yelpclass=db.yelpclassification



def review_to_wordlist( review, remove_stopwords=False ):
    # 1. Remove non-letters
        review_text = re.sub("[^a-zA-Z]"," ", review)
    # 2. Convert words to lower case and split them
        words = review_text.lower().split()    #
    # 3. Optionally remove stop words (false by default)
        if remove_stopwords:
            stops = set(stopwords.words("english"))
            words = [w for w in words if not w in stops]
    # 4. Return a list of words
        return(words)


revlist=yelpclass.find({},{"_id":0,"text":1,"city":1})
data  = pd.DataFrame(list(revlist))

print(data.shape)

# Generate the training set 80/20 using cross validation train test .  
train = data.sample(frac=0.8, random_state=1)
# Select anything not in the training set and put it in the testing set.
test = data.loc[~data.index.isin(train.index)]
# Print the shapes of both sets.
print(train.shape)
print(test.shape)

 # Initialize an empty list to hold the clean reviews
clean_train_reviews = []
    
    
# Create an empty list and append the clean reviews one by one
for row_index, row in train.iterrows():
    clean_train_reviews.append(" ".join(review_to_wordlist(train["text"][row_index], True)))
    
#similar for test set
clean_test_reviews = []

for row_index, row in test.iterrows():
    clean_test_reviews.append(" ".join(review_to_wordlist(test["text"][row_index], True)))



vectorizer = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000)

# fit_transform() does two functions: First, it fits the model
    # and learns the vocabulary; second, it transforms our training data
    # into feature vectors. The input to fit_transform should be a list of
    # strings.
train_data_features = vectorizer.fit_transform(clean_train_reviews)
vocab = vectorizer.get_feature_names()

    # Convert the result to an array
train_data_features = train_data_features.toarray()

 # Initialize a Random Forest classifier with 100 trees
forest = RandomForestClassifier(n_estimators = 100)

# Fit the forest to the training set, using the bag of words as
    # features and the sentiment labels as the response variable
forest = forest.fit( train_data_features, train["city"] )

# Get a bag of words for the test set, and convert to a numpy array
test_data_features = vectorizer.transform(clean_test_reviews)
test_data_features = test_data_features.toarray()

    # Using random forest to make sentiment label predictions

result = forest.predict(test_data_features)

score= accuracy_score(result,test["city"])

print(score)

#feature importance
"""
feature_importance = forest.feature_importances_
#descending oreder sorting
indices = np.argsort(feature_importance)[::-1]
print("Feature ranking:")
#train_data_features.shape[1]
#first 20 features
for f in range(20):
    print("%d.  %s (%f)" % (f + 1, vocab[indices[f]], feature_importance[indices[f]]))
"""

#Word Cloud tagging for city features, concentrating on the city with label 1
revlisttag1=yelpclass.find({"city":1},{"_id":0,"text":1,"city":1})
data1  = pd.DataFrame(list(revlisttag1))
tag_reviews1 = []

  
revlisttag0=yelpclass.find({"city":0},{"_id":0,"text":1,"city":1})
data0  = pd.DataFrame(list(revlisttag0))
tag_reviews0 = []


for row_index, row in data1.iterrows():
    tag_reviews1.append(" ".join(review_to_wordlist(data1["text"][row_index], True)))


for row_index, row in data1.iterrows():
    tag_reviews0.append(" ".join(review_to_wordlist(data0["text"][row_index], True)))
    
  


vectorizer1 = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000)

tag_reviews1_features = vectorizer1.fit_transform(tag_reviews1)
vocab1 = vectorizer.get_feature_names()
vocab1=list(vocab1)

vectorizer0 = CountVectorizer(analyzer = "word",   \
                             tokenizer = None,    \
                             preprocessor = None, \
                             stop_words = None,   \
                             max_features = 5000)

tag_reviews0_features = vectorizer0.fit_transform(tag_reviews0)
vocab0 = vectorizer0.get_feature_names()
vocab0=list(vocab0)    
    
    
common_test_reviews=[]
#using set operation for getting common features
common_test_reviews=list(set(vocab1) & set(vocab0))

#print(common_test_reviews)
#deleting common features
tag_reviews1_clean = [i for i in vocab1 if i not in common_test_reviews]

tag_reviews0_clean = [i for i in vocab0 if i not in common_test_reviews]

str1=" ".join(tag_reviews1_clean)
str0=" ".join(tag_reviews0_clean)

#for label 1
wordcloud_tag1 = WordCloud(max_words=500,width=1600,height=900).generate(str1)
plt.imshow(wordcloud_tag1)
plt.axis("off");

#wordcloud_tag0 = WordCloud(max_words=500,width=800,height=500).generate(str0)
#plt.imshow(wordcloud_tag0)
#plt.axis("off");

print ("End: "+time.strftime("%I:%M:%S")) 
