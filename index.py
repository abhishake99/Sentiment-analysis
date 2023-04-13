import pickle
import re
import json
import spacy
import string
import nltk
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from nltk.corpus import wordnet
from cleantext import clean
from sklearn.pipeline import Pipeline, make_pipeline
import streamlit as st

CLEANR = re.compile('<.*?>') 
en = spacy.load('en_core_web_sm')
stopwords = en.Defaults.stop_words
punc=string.punctuation
lemmatizer = WordNetLemmatizer()
def punc_remover(text):
    for i in text:
        i[0]=str(i[0])
        for j in i[0]:
            if j in punc:
                i[0]=i[0].replace(j,'')
    return text

def lowercase_list(lst):
    
    for i in  lst:
        i[0]=str(i[0])
        i[0]=np.char.lower(i[0])
    return lst

def stopwords_remover(text):
    for i in text:
        i[0]=str(i[0])
        split_text=i[0].split()
        new_text=[]
        for j in split_text:
            if j not in stopwords:
                new_text.append(j)
        i[0]= " ".join(new_text)
    return text        

def remove_emojis(data):
    emoj = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"  # chinese char
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642" 
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                      "]+", re.UNICODE)
    for i in data:
        i[0]=str(i[0])
        i[0]=re.sub(emoj, '', i[0])
    return data            

def cleanhtml(raw_html):
   for i in raw_html:
        i[0]=str(i[0])
        i[0] = re.sub(CLEANR, '', i[0])
   return raw_html

def get_simple_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def lemmatizerrr(text):
    for i in text:
        i[0]=str(i[0])
        split_text=i[0].split()
        new_text=[]
        for j in split_text:
            tag=pos_tag([j])
            lemmatizer.lemmatize(j,pos=get_simple_pos(tag[0][1]))
        i[0]= " ".join(split_text)
    return text 

def othercleaning(tweet):
    for i in tweet:
        i[0]=str(i[0])
        i[0] = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',i[0]) #remove links
        i[0] = re.sub('@[^\s]+','',i[0]) #remove usernames
        i[0] = re.sub('[\s]+', ' ', i[0])
    return tweet       

with open('pipeline1.pkl', 'rb') as f1:
    pipeline1 = pickle.load(f1)
with open('pipeline2.pkl', 'rb') as f2:
    pipeline2 = pickle.load(f2)
    
st.title("Sentiment Predictor")
input_sms = st.text_area("Enter the message")
if st.button('Predict'):
    trans=pipeline1.transform(np.array(input_sms).reshape(-1,1))
    pre=pipeline2.predict(trans[0])
    if pre[0] == 'positive':
        st.header("Positive")
    elif pre[0] == 'negative':
        st.header("Negative")
    else:
        st.header("Neutral")
