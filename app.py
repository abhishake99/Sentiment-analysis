import pickle
from keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import streamlit as st
import time

# with st.echo():
#         @st.cache_resource
#         options = Options()
#         options.add_argument("--headless")
#         options.add_argument("--no-sandbox")
#         options.add_argument("--disable-dev-shm-usage")
#         options.add_argument("--disable-gpu")
#         options.add_argument("--disable-features=NetworkService")
#         options.add_argument("--window-size=1920x1080")
#         options.add_argument("--disable-features=VizDisplayCompositor")

        #options = Options()
        #options.add_argument('--disable-gpu')
        #options.add_argument('--headless')
        #options.add_argument("--window-size=1366,768")
        #options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
        #driver=webdriver.Chrome(executable_path="/Users/abhishek/.wdm/drivers/chromedriver/win32/113.0.5672.63/chromedriver.exe", options=options)        
        #wait = WebDriverWait(driver, 30)

class MyTwitter:
    
    def __init__(self,emailg,passwordg,usernameg,choice,ini):
        self.emailg=emailg
        self.passwordg=passwordg
        self.usernameg=usernameg
        self.choice=choice
        self.ini=ini
    
    def execute_driver(self):
        driver = webdriver.Chrome(executable_path = "/Users/abhishek/.wdm/drivers/chromedriver/win32/113.0.5672.63/chromedriver.exe")
        wait = WebDriverWait(driver,10)  
        return driver 
    
    def selection(self,property,driver):
        
        time.sleep(2)
        driver.find_element(By.XPATH,property).send_keys(self.ini)
        #driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[3]/div").click()
        driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[6]/select/option[12]").click()
        driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[1]/div/div/div/div/div/div[3]/div").click()
        time.sleep(2)
        driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[2]/a").click()
        
    def fetch_tweets(self,driver):
        #collector=[]
        #while len(collector)<10:
        #    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
        time.sleep(6)
        alltweets=driver.find_elements(By.XPATH,"//*[@class='css-901oao r-1nao33i r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0']")
        
        #prevlength=len(alltweets)
        # while(len(alltweets)!=10):
        #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
        #     prevlength=len(alltweets)
        #     time.sleep(7)
        #     alltweets=driver.find_elements(By.XPATH,"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div/div/div/article")
        #     if len(alltweets)<=prevlength:
        #         break
        #alltweets=driver.find_elements(By.XPATH,"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/section/div/div/div/div/div/article")
        tweetlist=[]
        for i in alltweets:
            tweet=i.find_elements(By.XPATH,".//span")
            tweetstr=""
            for j in tweet:
                tweetstr+=j.text
            tweetlist.append(tweetstr)
        return tweetlist
    def search_query(self,driver):
        driver.get("https://twitter.com/search?q=yo&src=typed_query")
        time.sleep(2)
        driver.get_screenshot_as_file("screenshot.png")
        
        driver.find_element(By.XPATH,"//*[@data-testid='searchFiltersAdvancedSearch']/a").click()
        if self.choice == 'randomword':
            self.selection("/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[1]/div/label/div/div[2]/div/input",driver)
        elif self.choice == 'account':
            self.selection("/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[5]/div[1]/div/label/div/div[2]/div/input",driver)
        else:
            self.selection("/html/body/div[1]/div/div/div[1]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[2]/div/div[2]/div[5]/div/label/div/div[2]/div/input",driver)
        time.sleep(6)
        finaltweets=self.fetch_tweets(driver)
        #driver.quit() 
        return finaltweets
        
    
    def login(self,driver):
        #driver=self.execute_driver()
        driver.get("https://twitter.com")
        time.sleep(5)
        login1=driver.find_elements(By.XPATH,"/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/div/div/div[2]/div/div/div[1]/a")
        if len(login1)>0:
            login1[0].click()
            time.sleep(2)
        email=driver.find_element(By.XPATH,"/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input")
        email.send_keys(self.emailg)
        next=driver.find_element(By.XPATH,"/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]")
        next.click()
        time.sleep(3)
        username=driver.find_elements(By.XPATH,"/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[2]/label/div/div[2]/div/input")
        if len(username)>0:
            username[0].send_keys(self.usernameg)
            driver.find_element(By.XPATH,"/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div").click()
            time.sleep(3)
        password=driver.find_element(By.XPATH,"/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input")
        password.send_keys(self.passwordg)
        login=driver.find_element(By.XPATH,"/html/body/div/div/div/div[1]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div/div")
        login.click()
        time.sleep(5)
        #return self.search_query(driver)
        # driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/header/div/div/div/div[1]/div[2]/nav/a[2]/div").click()
        # search_input=driver.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input")
        # search_input.send_keys("yo")
       
    
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
task2="Work with Twitter"
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
    st.header("Please select what do you want to search?")
    t1="Search tweets related to some random word"
    t2="Search tweets for a account"
    t3="Search tweets according to some hashtag"
    desiretweet=st.radio("Choose your desired option please:-",(t1,t2,t3))  
    collectedtweetslist=[]
    def inputs(desiretweet):
        if desiretweet==t1:
            ini=st.text_input("Enter the Word")
            choice='randomword'
        if desiretweet==t2:
            ini=st.text_input("enter the account")
            choice='account'
        if desiretweet==t3:
            ini=st.text_input("enter the hashtag")
            choice='hashtag'
        return ini,choice
    def print_tweets(collectedtweetslist):
        for i in collectedtweetslist:
            pre,prob=predict_class([i])
            if pre == 'Positive':
                st.header("Positive")
                st.subheader("Tweet :{val}".format(val=i))
                st.subheader("Percentage of Positivity : {prob}".format(prob=prob))
            elif pre == 'Negative':
                st.header("Negative")
                st.subheader("Tweet :{val}".format(val=i))
                st.subheader("Percentage of Negativity : {prob}".format(prob=prob))
            else:
                st.header("Neutral")
                st.subheader("Tweet :{val}".format(val=i))
                st.subheader("Percentage of Neutrality : {prob}".format(prob=prob))
    ini,choice=inputs(desiretweet)
    def collect_credentials():
        username = st.text_input("Username:")
        password=st.text_input("Password")
        Email =st.text_input("Email Address")
        return username,password,Email
    username,password,Email=collect_credentials()
    if username!='' and password!='' and Email!='':  
        if st.button("Start process"):
            
            instance=MyTwitter(Email,password,username,choice,ini)
            driver=instance.execute_driver()
            driver.maximize_window()
            instance.login(driver)
            collectedtweetslist=instance.search_query(driver)
            print_tweets(collectedtweetslist)
        
        if len(collectedtweetslist)>0:
            if st.button("Want to do more?"):
                #desiretweet=st.radio("Choose your desired option please:-",(t1,t2,t3))
                ini,choice=inputs(desiretweet)
                collectedtweetslist=instance.search_query(driver)
                print_tweets(collectedtweetslist)
                # if st.button('STOP'):
                #     driver.quit()
                #     break
    else:
        st.markdown("Enter the credentials properly")
    #driver.quit()
#if st.button('Predict sentiments by accessing twitter api'):
#    st.header("entered twitter api")
