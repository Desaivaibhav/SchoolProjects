# -*- coding: utf-8 -*-
"""
Created on Sat Nov 29 17:28:53 2016

making collection of city and review in binary format
selected city with label 1 and rest cities with label 0
balanced dataset 6000 with value 1 and 6000 with value 0
"""


import pymongo
from pymongo import MongoClient
import datetime
import time 

print ("Start: "+time.strftime("%I:%M:%S")) 
client = MongoClient('localhost', 27017)
db = client.yelp #Database
#collection
yelpreview=db.yelp_review
dropresult=db.yelpclassification.drop()
def get_reviewset(city,cnt,val):
    rec=0
    yelptext=yelpreview.find({"city":city},{"_id":0,"text":1,"city":1}).limit(cnt)
    for y in yelptext:
        db.yelpclassification.insert_one({"text":y['text'],"city":val})
        rec+=1
    print (rec)
    return rec


def run(city_val):
      
    if city_val=="":
        cityval="Pittsburgh"
    else:
        cityval=city_val


    reccnt=get_reviewset(cityval,6000,1)
    city_list=list(yelpreview.distinct( "city" ))
    for c in city_list:
        if c != cityval:
            print(c)
            reccnt=get_reviewset(c,1000,0)
        
    print ("End: "+time.strftime("END"+"%I:%M:%S"))
    
if __name__ == "__main__":
    citydata=run("Glendale")