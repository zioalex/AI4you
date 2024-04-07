import requests
import json
import time
import argparse
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import re
import pickle
from collections import Counter
from nltk.corpus import stopwords
from textblob import TextBlob
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB

# import nltk
# nltk.download('stopwords')


def get_data(url):
 chrome_options = Options()
 chrome_path = "/opt/chrome-linux64/chrome"
 chrome_options.binary_location = chrome_path
 # Set up Chrome options
 s = Service("/opt/chromedriver-linux64/chromedriver")

 print("URL:", url)
 driver = webdriver.Chrome(service=s, options=chrome_options)
 wait = WebDriverWait(driver, 10)
 # make a request to the given url and save it as response object
 driver.get(url)                                    
 wait.until(EC.url_to_be(url))
 get_url = driver.current_url
 print("The current url is:"+str(get_url))
 html_content = driver.page_source                         
 print(html_content)
 soup = BeautifulSoup(html_content, 'html.parser')                                                                                      
 data = soup.find('div', {'id': 'quote-display'}) #.find('span').get_text()                                                               
 return data, driver.quit()                                         

def parse_command_line_arguments():                                            
 parser = argparse.ArgumentParser(description='Python crypto trading bot using sentiment analysis')                                                           
 parser.add_argument('--mode', type=str, default="train", help="Set mode (train/predict)")                                                                    
 args = parser.parse_args()                                                    
 return args                                                                   

def preprocess_data():                                                         
	stop_words = set(stopwords.words("english"))
	data = []                                                                     
	labels = []                                                                   
	#urls = [r'https:\/\/www.coinbase.com\/price\/\w+' for _ in range(20)] # replace with actual list of URLs                                                     
	urls = ['https://www.coinbase.com/explore/'] # replace with actual list of URLs                                                     
	for url, _ in get_data_and_parse_sentiment(urls):
		print("URL:",url)
		data.append(url)                                                              
		labels.append('positive' if TextBlob(url).sentiment.polarity > 0 else 'negative')
	X, y = np.array(data), np.array(labels)
	return X, y                                                                   

def train_model(X, y):                                                         
 tfidf_vectorizer = TfidfVectorizer()                                          
 X_tfidf = tfidf_vectorizer.fit_transform(X)
 x_train, x_test, y_train, y_test = train_test_split(X_tfidf, y, test_size=0.2, random_state=42)                                                              
 clf = MultinomialNB()                                                         
 clf.fit(x_train, y_train)                                                     
 return clf, tfidf_vectorizer                                                  

def get_data_and_parse_sentiment(urls):
	print("URLS:",urls)
	sentiment_scores = []                                                         
	for url in urls:                                                              
		print(f"Scraping url {url}")
		data = get_data(url)                                                       
		sentiment_score, _ = analyze_sentiment(data)
		sentiment_scores.append((data, sentiment_score))
	return sentiment_scores                                                       

def main():                                                                    
	args = parse_command_line_arguments()                                         
	if args.mode == "train":                                                      
		X, y = preprocess_data()                                                      
		clf, tfidf_vectorizer = train_model(X, y)
		with open('clf_model.pkl', 'wb') as file:
			pickle.dump(clf, file)
		with open('tfidf_vectorizer.pkl', 'wb') as file:
			pickle.dump(tfidf_vectorizer, file)
	else: # predict mode                                                          
		clf = pickle.load(open("clf_model.pkl", "rb"))
		tfidf_vectorizer = pickle.load(open("tfidf_vectorizer.pkl", "rb"))
		data = input("Enter coin URL to predict sentiment: ")
		X_test = [tfidf_vectorizer.transform([data])]                                 
		prediction = clf.predict(X_test)[0]                                           
		print(f"Prediction for {data}: {prediction}")                                 
                                                                               
if __name__ == "__main__":                                                     
 main()                                                                                                                                                       

