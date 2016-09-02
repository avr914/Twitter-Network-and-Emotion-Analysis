# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 16:31:40 2015

@author: arvind
"""

import tweepy
import keys

CONSUMER_KEY = keys.CONSUMER_KEY
CONSUMER_SECRET = keys.CONSUMER_SECRET
ACCESS_TOKEN = keys.ACCESS_TOKEN
ACCESS_TOKEN_SECRET = keys.ACCESS_TOKEN_SECRET
auth = tweepy.OAuthHandler(CONSUMER_KEY,CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)

api = tweepy.API(auth)

#user = api.me()
#print "Follower Count: " + str(user.followers_count)
#print "Friend Count: " + str(user.friends_count)

logfile = open('testlog','wb')


mentions = api.mentions_timeline()

for mention in mentions:
    print "User: %s" % (mention.user.screen_name)
    logfile.write(str(mention.user.screen_name) + '\n')
    print "Mention text: %s" % (mention.text)
    logfile.write(str(mention.text) + '\n')
    entities = mention.entities
    user_mentions = entities['user_mentions']
    #print "user_mentions: " + str(mention.entities)
    for usr in user_mentions:
        print usr['screen_name']
        logfile.write(usr['screen_name'])
    #print user_mentions

logfile.flush()
logfile.close()
    
