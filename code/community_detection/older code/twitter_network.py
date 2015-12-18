# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 08:06:11 2015

@author: arvind
"""

import tweepy
import emotion
import sqlite3 as lite
import sys
import time
import os
import json
import argparse
import csv

# Twitter Credentials
CONSUMER_KEY = 'XRH8Wd2ZaDhAUmA5kEY5qGTrp'
CONSUMER_SECRET = '0rWg61r9DOMGFLXq5ebgLnDRC8xHqV1dgZYyaPVdwGO0sa6f4v'
ACCESS_TOKEN = '3154159514-wPdXqU9ayRiFEkzjfHVmFqVuDzQdK5SYJbsymH6'
ACCESS_TOKEN_SECRET = 'KzRfzz9AHDkjB2r15dPsXcaqxzzkSGF5qDeTtnRveOEDn'

# OAuth Authentication
auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

# Encode string into ascii
enc = lambda x: x.encode('ascii', errors='ignore')


tweepy.Cursor(api.user_timeline, id="twitter")

logfile = open('logfile.log','wb')
csvwriter = csv.writer(logfile)


con = None
try:
    con = lite.connect('sentiment_dict.sqlite')
    cur = con.cursor()
    for row in cur.execute('SELECT user FROM test_accounts'):        
        try:                
            public_tweets = api.user_timeline(screen_name=str(row[0]),count=20)              
            file.write("%s:\n" % row[0])
            for tweet in public_tweets:
                file.write(tweet.text.encode('utf-8'))
                file.write("\n")
                file.write(str(emotion.measureEmotion(tweet.text)))
                file.write("\n")
                #print "tweet: " + unicode(tweet.text)
                #print emotion.measureEmotion(tweet.text)
                
        except tweepy.TweepError, e:   
            print "Error: %s:" % e.args[0]
            pass

except lite.Error, e:
    print "Error: %s:" % e.args[0]
    sys.exit(1)
finally:
    logfile.flush()
    logfile.close()
    if con:
        con.close()
#tweepy.Cursor(api.user_timeline, id="twitter")
#for page in tweepy.Cursor(api.user_timeline).pages():
#for tweet in page:
#print "|||>user: %s\ntweet: %s" % (unicode(tweet.user.screen_name),unicode(tweet.text))
#print emotion.measureEmotion(tweet.text)
