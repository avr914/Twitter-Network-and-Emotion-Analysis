# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 05:17:59 2015

@author: arvind
"""
import sqlite3
import sys
import re
from scipy import stats
from scipy.stats import norm
from afinn import Afinn
#V.Mean.Sum, V.SD.Sum, A.Mean.Sum, A.SD.Sum
def measureEmotion(sentence):
    con = None
    #splitting sentence
    sentence_list = re.findall(r'[^\s!,.?":;0-9]+',sentence)
    count = 0
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
                count += 1
            
    except sqlite3.Error, e:
        print "Error: %s:" % e.args[0]
        sys.exit(1)
    finally:
        if con:
            con.close()
    
    afinn = Afinn()
    if count < 1 or weighted_val_dividend == 0:
        return (afinn.score(sentence),0.0)        
    valence_mean = weighted_val_sum/weighted_val_dividend
    arousal_mean = weighted_aro_sum/weighted_aro_dividend
    return (valence_mean,arousal_mean)
