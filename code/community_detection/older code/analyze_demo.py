# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 05:17:59 2015

@author: arvind
"""
import sqlite3
import sys
import re
import time
from scipy import stats
from scipy.stats import norm
from afinn import Afinn
#V.Mean.Sum, V.SD.Sum, A.Mean.Sum, A.SD.Sum
def measureEmotion(sentence):
    con = None
    start_time = time.time()
    #splitting sentence
    sentence_list = re.findall(r'[^\s!,.?":;0-9]+',sentence)
    weighted_val_sum = 0
    weighted_val_dividend = 0
    weighted_aro_sum = 0
    weighted_aro_dividend = 0
    print sentence
    try:
        con = sqlite3.connect('sentiment_dict.sqlite')
        cur = con.cursor()
        for part in sentence_list:
            cur.execute("SELECT valence_mean, valence_sd, arousal_mean, arousal_sd FROM sentiment_dictionary WHERE word=?",(part,))
            data = cur.fetchone()
            if data != None:
                val = data[0]
                val_weight = norm(val,data[1]).pdf(val)
                weighted_val_sum += val*val_weight
                weighted_val_dividend += val_weight
                aro = data[2]
                aro_weight = norm(aro,data[3]).pdf(aro)
                weighted_aro_sum += aro*aro_weight
                weighted_aro_dividend += aro_weight
            
    except sqlite3.Error, e:
        print "Error: %s:" % e.args[0]
        sys.exit(1)
    finally:
        if con:
            con.close()
    
    afinn = Afinn()
    if weighted_val_dividend == 0:
        print "AFINN Sentiment Score: " + str(afinn.score(sentence))
        return
    valence_mean = weighted_val_sum/weighted_val_dividend
    arousal_mean = weighted_aro_sum/weighted_aro_dividend
    print "Valence Mean: " + str(valence_mean)
    print "Arousal Mean: " + str(arousal_mean)
    elapsed_time = (time.time() - start_time)
    print "Elapsed_time: %s" % (elapsed_time)

sentence_in = raw_input("Enter a tweet (140 characters or less):")
measureEmotion(sentence_in)