# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 16:31:40 2015

@author: arvind
"""

import tweepy

consumer_key = 'XRH8Wd2ZaDhAUmA5kEY5qGTrp'
consumer_secret = '0rWg61r9DOMGFLXq5ebgLnDRC8xHqV1dgZYyaPVdwGO0sa6f4v'
access_token = '3154159514-wPdXqU9ayRiFEkzjfHVmFqVuDzQdK5SYJbsymH6'
access_token_secret = 'KzRfzz9AHDkjB2r15dPsXcaqxzzkSGF5qDeTtnRveOEDn'
auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_token_secret)

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
    
