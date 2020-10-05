import json
import streamlit as st
import nltk
from nltk import sent_tokenize
from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
stopwordsE = stopwords.words("English")

#funtio to read from json files
def read_from_file(file_name):
    with open(file_name,"r") as read_file:
        data=json.load(read_file)
        print("You successfully read from {}.".format(file_name))
        return data
# function to save json files
def save_to_file(data,file_name):
    with open(file_name,"w") as write_file:
        json.dump(data,write_file,indent=2)
        print("You successfully saved to {}.".format(file_name))

# Function to extract all the text in the abstract field of all the articles
def allAbstWords(article: dict):
    longString = ""
    for i in article["results"]:
        longString += i["abstract"]
    return longString

# Function to obtain the top words
def topWords(sentence, quantity : int):
    words = word_tokenize(sentence)
    words_no_punc =[]
    for w in words:
        if w.isalpha():
            words_no_punc.append(w)

    clean_words = []
    for w in words_no_punc:
        if w not in stopwordsE:
            clean_words.append(w)

    fDist = FreqDist(clean_words)
    return fDist.most_common(quantity)