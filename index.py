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
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('corpus')

CLEANR = re.compile('<.*?>') 
en = spacy.load('en_core_web_sm')
stopwords = en.Defaults.stop_words
punc=string.punctuation
lemmatizer = WordNetLemmatizer()
def lowern(text):
    text=text.lower()
    return text
def punc_remover(text):
    for i in text:
        if i in punc:
            text=text.replace(i,'')
    return str(text)

def stopwords_remover(text):
    text=str(text)
    split_text=text.split()
    new_text=[]
    for i in split_text:
        if i not in stopwords:
            new_text.append(i)
    return " ".join(new_text)        

def remove_emojis(text):
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
    return re.sub(emoj, '', text)            

# def spell_correct(text):
#     text=str(text)
#     textblb=TextBlob(text)
#     return textblb.correct().string 

def cleanhtml(text):
    cleantext = re.sub(CLEANR, '', text)
    return cleantext

def get_simple_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def lemmatizerrr(sentence):
    nltk_tagged = nltk.pos_tag(nltk.word_tokenize(sentence))  
    wordnet_tagged = map(lambda x: (x[0], get_simple_pos(x[1])), nltk_tagged)
    lemmatized_sentence = []
    for word, tag in wordnet_tagged:
        if tag is None:
            lemmatized_sentence.append(word)
        else:        
            lemmatized_sentence.append(lemmatizer.lemmatize(word, tag))
    return " ".join(lemmatized_sentence)

def othercleaning(text):
    text = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','',text) #remove links
    text = re.sub('@[^\s]+','',text) #remove usernames
    text = re.sub('[\s]+', ' ', text)
    return text 
def masterfunction(text):
    text=lowern(text)
    text=punc_remover(text)
    text=stopwords_remover(text)
    text=remove_emojis(text)
    text=cleanhtml(text)
    text=lemmatizerrr(text)
    text=othercleaning(text)
    return text              

with open('pipeline2upn.pkl', 'rb') as f2:
    pipeline2 = pickle.load(f2)
    
st.title("Sentiment Predictor")
input_sms = st.text_area("Enter the message")
if st.button('Predict'):
    trans=masterfunction(input_sms)
    pre=pipeline2.predict([trans])
    if pre[0] == 'positive':
        st.header("Positive")
    elif pre[0] == 'negative':
        st.header("Negative")
    else:
        st.header("Neutral")

