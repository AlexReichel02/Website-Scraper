from newspaper import Article
import requests
from bs4 import BeautifulSoup
import re
import pytz
import datetime
import platform
from readability.readability import Document as Paper
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import nltk
from selenium import webdriver
from tkinter import *
import tkinter as tk
from tkinter import messagebox
from selenium.webdriver.support.ui import WebDriverWait
import random 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from wordcloud import WordCloud
import scrapy
import csv
import time
nltk.download('punkt')
#from requests.packages.urllib3.exceptions import InsecureRequestWarning

def summarize(text, per):
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(text)
    tokens=[token.text for token in doc]
    word_frequencies={}
    for word in doc:
       
        if word.text.lower() not in STOP_WORDS:
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():                            
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    #print(summary)
    return summary

def display_response():
    global allText
    global allKeywords
    global summary
    url = URLField.get()
#url = input("Enter URL: ")
    try:
        article = Article(url)
        article.download()
        article.parse()
        article.nlp()
        list = article.keywords
        allKeywords = list
        #for l in list:
        #print(l)
        allText = article.text
        #print(article.text)
        response = summarize(article.text,1)
        summary = response
        messagebox.showinfo("Information","Website Scan complete, Click any button or enter new website")
    except ValueError:
        print('Error downloading the page.')
        messagebox.showinfo("Information","Website format not recognized, Try another")

def displaySummary():
    OutputField.config(state='normal')
    OutputField.delete(1.0, tk.END)
    OutputField.insert(tk.END, summary)
    OutputField.config(state='disabled')

def displayText():
    OutputField.config(state='normal')
    OutputField.delete(1.0, tk.END)
    OutputField.insert(tk.END, allText)
    OutputField.config(state='disabled')

def clearText():
  URLField.delete(0,'end')


def displayKeywords():
    OutputField.config(state='normal')
    OutputField.delete(1.0, tk.END)
    OutputField.insert(tk.END, allKeywords)
    OutputField.config(state='disabled')


def extract(url):
    elem = None
    location_of_chrome_driver='/Users/alexreichel/Downloads/chromedriver_mac64/chromedriver'
    service = Service(executable_path=location_of_chrome_driver)
    driver = webdriver.Chrome(service=service)
    driver.get(url)

    try:
        found = WebDriverWait(driver, 10).until(
            EC.visibility_of(
                driver.find_element(By.TAG_NAME, "body")
            )
        )
        # Make a copy of relevant data, because Selenium will throw if
        # you try to access the properties after the driver quit
        elem = {
          "text": found.text
        }
    finally:
        driver.close()

    return elem

def transform(elem):
    return elem["text"]
        
def JavaResponse():
    if __name__ == "__main__":
        url = URLField.get()
        #url = "https://alexreichelportfolio.com/"

    elem = extract(url)
    if elem is not None:
        text = transform(elem)
        #print(text)
        response = summarize(text,0.5)
        OutputField.config(state='normal')
        OutputField.delete(1.0, tk.END)
        OutputField.insert(tk.END, response)
        OutputField.config(state='disabled')
    else:
        print("Sorry, could not extract data")


root = tk.Tk()
root.title("Scraper")
root.geometry("1200x800")
allText =''
allKeywords=[]
summary=''

URLField = tk.Entry(root, font=("Arial", 14))
URLInputLabel =  Label( root , text = "Enter Website" )
URLInputLabel.grid(row = 5, column = 0)
URLField.grid(row = 5, column = 1)

submit_button = tk.Button(root, text="Get Java Data", font=("Arial", 14),command=JavaResponse)
submit_button.grid(row = 11, column = 0, sticky = W)

submit_button = tk.Button(root, text="Get Data", font=("Arial", 14),command=display_response)
submit_button.grid(row = 6, column = 0, sticky = W)

submit_button = tk.Button(root, text="Show summary", font=("Arial", 14),command=displaySummary)
submit_button.grid(row = 7, column = 0, sticky = W)

submit_button = tk.Button(root, text="Show keywords", font=("Arial", 14),command=displayKeywords)
submit_button.grid(row = 8, column = 0)

submit_button = tk.Button(root, text="Show whole text", font=("Arial", 14),command=displayText)
submit_button.grid(row = 9, column = 0)

submit_button = tk.Button(root, text="Clear Website", font=("Arial", 14),command=clearText)
submit_button.grid(row = 10, column = 0)


OutputField = tk.Text(root, font=("Arial", 12), state='disabled')
OutputField.grid(row = 25, column = 3)
root.mainloop()

