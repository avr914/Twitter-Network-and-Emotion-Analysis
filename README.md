Twitter Network and Emotion Analysis
===================


This is my personal research project into Twitter that I completed as part of CS 196. My research was more of personal exploration into the cool data trends you could discover by processing Twitter data. Most of the work is split into two subjects: Emotion/Sentiment analysis, and Community Detection.

----------

Emotion/Sentiment Analysis
-------------

### Topic Introduction (aka the boring stuff)
When I first started looking into Twitter, one of my first interests was seeing if there was a way to determine whether a tweet most strongly represents one emotion. Classifying emotions actually involves a fair amount of difficulty simply due to the ambiguity by which you classify emotions. In fact, emotion analysis of text is by and large a very poorly explored topic. There are not many companies, products or research looking into this field from a computation point of view. Rather, sentiment analysis is quite popular. Products like SentiStrength, Alchemy API, and NLTK have established and well functioning modules for judging whether some small corpus or sample of a corpus express positive or negative sentiment. So I began my research here.

#### Sentiment Analysis
In essence, sentiment analysis is usually modeled as a 1-D problem where the sentiment is expressed on one axis going negative to positive, where a score of 0 is roughly neutral or ambiguous. In sentiment analysis, this score is termed the *valence* score. There are a few approaches to solving this problem.

##### Machine Learning
The most popular products such as SentiStrength and AlchemyAPI use machine learning to solve this problem. When I was working on this project, I didn't have any exposure with machine learning, so I mainly used these to benchmark my approaches, rather than attempt to reimplement or use my own implementation of a learning algorithm for them.
##### Word Dictionary
Some papers describe determining sentiment using a word dictionary style approach. Most of these papers based their work off of formal ANEW-style dictionaries. One of the more intriguing ones was the AFINN project, which was a sentiment dictionary project created for frequently used Twitter terms that performed fairly well in the domain of tweets. 
