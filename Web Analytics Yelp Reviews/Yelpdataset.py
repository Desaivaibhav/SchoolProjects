# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 12:26:19 2016
Yelp data set preparation
"""

import pymongo
from pymongo import MongoClient
import datetime
import time 

print ("Start: "+time.strftime("%I:%M:%S")) 
client = MongoClient('localhost', 27017)
db = client.yelp #Database
#collections
review=db.review
business=db.business

#get the required data focussing on US cities   and restaurant category focussing on businesses having reviews more than 100
business_list=list(business.find({'$and':[{"city":{'$in':["Glendale","Boulder City","Harrisburgh","Peoria","Madison","Tempe","Pittsburgh","Charlotte","Phoneix","Las Vegas"]}},{"categories":{'$in':["Restaurants"]}},{"review_count":{'$gt':100}}]},{"_id":0,"business_id":1,"city":1,"categories":1,"review_count":1}))

for b in business_list:
         revw_list=review.find({"business_id":b['business_id']},{"_id":"0","business_id":"1","stars":"1","text":"1","date":"1"})
         for r in revw_list:
             result = db.yelp_review.insert_one({"business_id":b['business_id'],"city":b['city'],"text":r['text']})
             #print("business_id:"+str(b['business_id']))
             #print("city:"+str(b['city']))
             #print("stars:"+str(r['stars']))
             #print("text:"+str(r['text']))
print ("End: "+time.strftime("%I:%M:%S")) 