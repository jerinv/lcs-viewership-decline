# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 18:16:43 2021

@author: jerin
"""

import praw
import pandas as pd
import re

import nltk
from nltk.corpus import stopwords

import numpy as np
from PIL import Image
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

# =============================================================================
# EXTRACT DATA FROM REDDIT THREAD
# =============================================================================

# Initiate reddit API object, no credentials needed for public threads
reddit = praw.Reddit(
    user_agent="Comment Extraction (by u/jerbearr93)",
    client_id="IJOLQs-tCLTCkVIKQ9jZRw",
    client_secret="1Nkg0SGt2N7Dnn_6cPAf4ThMq9NVuQ",
)

# Get league of legends submission link https://www.reddit.com/r/leagueoflegends/comments/pf0rwq/the_2021_lcs_summer_split_had_the_lowest_peak/
submission = reddit.submission(id='pf0rwq')


submissionList = []
submission.comments.replace_more(limit=None)
for comment in submission.comments.list():
    submissionList.append(comment)
    
submissionText = [comment.body for comment in submissionList]

allComments = pd.DataFrame({'Comment':submissionText})
allComments.to_csv('data/comments.csv')

# =============================================================================
# PROCESS AND CLEAN TEXT FOR STOPWORDS AND PUNCTUATION
# =============================================================================
allCommentsString = ' '.join(submissionText)
allCommentsList = allCommentsString.split()

# Change all text to lowercase and remove punctuation
def clean_word(text):
    pattern = re.compile('[\W_]+')
    new_text = pattern.sub('', text).lower()
    return new_text
cleanWords = [clean_word(text) for text in allCommentsList]

# Create list of stopwords
nltk.download('stopwords')
english_stopwords = stopwords.words('english')
more_stopwords = list(STOPWORDS)
custom_stopwords = ['really','even','think','much','still','dont','im','thing','thats','lot','isnt','actually',
                    'theres','ive','got','game','watch','lcs','na','league','team','yeah','though','doesnt',
                    'games','teams','watching','people','go','didnt','youre','almost','v','etc','probably','especially',
                    'arent','come','want','something','take','say','stuff','keep','bit','said','find','fan','viewer',
                    'year','play','lol','cant','u','big','well','right','need','least','maybe','sure','many','way',
                    'make','made','one','give','top','theyre','work','things','literally','anymore','day','back','seem',
                    'see','less','us','last','makes','new','name','reason','pretty','final','going','vs','start',
                    'great','bad','better','never','used','around','fun','every','trying','years','first','good',
                    'fucking','best','viewership','viewers','feel','region','regions','hard','mean','number','fans',
                    'put','part','gets','always','either','numbers','feels','hes','might','saying','definitely',
                    'absolutely','getting','two','imo','know']

all_stopwords = set(english_stopwords + more_stopwords + custom_stopwords)

# Replace certain words that are unclean with better guess
def change_word(old_word, new_words):
    new_list = [i for i in cleanWords if i != old_word]
    new_list = new_list + new_words
    return new_list

cleanWords = change_word('world',['worlds'])
cleanWords = change_word('desk',['analyst','desk'])
cleanWords = change_word('internationally',['international'])
cleanWords = change_word('double',['doublelift'])
cleanWords = change_word('liftlift',['doublelift'])
cleanWords = change_word('bjergdoublelift', ['bjergsen','doublelift'])
cleanWords = change_word('bjergsen doublelift', ['bjergsen','doublelift'])
cleanWords = change_word('doublelift bjergsen', ['bjergsen','doublelift'])
cleanWords = change_word('doubleliftbjerg', ['bjergsen','doublelift'])
cleanWords = change_word('sneakymeteosdlifti', ['sneaky','meteos','doublelift'])
cleanWords = change_word('doublelift sneaky', ['doublelift','sneaky'])
cleanWords = change_word('bjerg', ['bjergsen'])
cleanWords = change_word('bjeg', ['bjergsen'])
cleanWords = change_word('dlbjerg', ['bjergsen','doublelift'])
cleanWords = change_word('bjerg dl', ['bjergsen','doublelift'])
cleanWords = change_word('dl', ['doublelift'])
cleanWords = change_word('dls', ['doublelift'])
cleanWords = change_word('dlsneaky', ['doublelift','sneaky'])
cleanWords = change_word('dl sneaky', ['doublelift','sneaky'])
cleanWords = change_word('meteoss', ['meteos'])
cleanWords = change_word('ballsmeteoshai', ['balls','meteos','hai'])
cleanWords = change_word('capsperkzhumanoidbjergsennisqylarssenjensenpoejizuke', ['caps','perkz','humanoid',
                                                                                  'bjergsen','nisqy','larssen','jensen',
                                                                                  'poe','jizuke'])

# =============================================================================
# CREATE WORDCLOUD
# =============================================================================
# Create single string  of all the words
all_words = ' '.join(cleanWords)

lcs_color = np.array(Image.open('images/lcs_custom.png'))


# Create WordCloud
wordcloud = WordCloud(width=800,
                      height=800,
                      background_color = 'black',
                      mask = lcs_color,
                      stopwords = all_stopwords,
                      collocation_threshold = 300,
                      min_font_size = 15,
                      colormap='terrain')
cloud = wordcloud.generate(all_words)

cloud_counts = wordcloud.process_text(all_words)

# Plot WordCloud
plt.figure(figsize=(10,10),
           facecolor=None)
plt.axis('off')
plt.tight_layout(pad=0)
plt.show()

wordcloud.to_file('images/lcs_decline_cloud.png')