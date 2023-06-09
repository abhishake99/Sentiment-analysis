import pickle
import tensorflow
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
import streamlit as st

model = load_model('best_model.h5')
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

def predict_class(text):
    '''Function to predict sentiment class of the passed text'''
    
    sentiment_classes = ['Negative', 'Neutral', 'Positive']
    max_len=50
    
    # Transforms text to a sequence of integers using a tokenizer object
    xt = tokenizer.texts_to_sequences(text)
    # Pad sequences to the same length
    xt = pad_sequences(xt, padding='post', maxlen=max_len)
    # Do the prediction using the loaded model
    pre=model.predict(xt)
    #print(pre)
    yt = pre.argmax(axis=1)
    return sentiment_classes[yt[0]],round(pre[0][yt[0]]*100,4)

    
st.title("Sentiment Predictor")
st.markdown("This sentiment app is trained on Bidirectional LSTM neural network with almost 1 Lakh texts. This app works by tokenzing the entered text into padded integer sequence and then send to model for prediction.")
#st.subheader("What do want to do? Click on your desired task button")
task1="Predict sentiment for some random text"
task2="Work with twitter api"
desire=st.radio("Choose your desired task please:-",(task1,task2))
if desire==task1:
    input_sms = st.text_area("Enter the message")
    if st.button('Predict'):
        pre,prob=predict_class([input_sms])
        if pre == 'Positive':
            st.header("Positive")
            st.subheader("Percentage of Positivity : {prob}".format(prob=prob))
        elif pre == 'Negative':
            st.header("Negative")
            st.subheader("Percentage of Negativity : {prob}".format(prob=prob))
        else:
            st.header("Neutral")
            st.subheader("Percentage of Neutrality : {prob}".format(prob=prob))
if desire==task2:
    st.header("Currently in development stage")
    # consumerKey = st.text_input("consumer_key")
    # consumerSecret = st.text_input("consumer_key_secret")
    # accessToken = st.text_input("access_token")
    # accessTokenSecret = st.text_input("access_token_secret")
