import requests
import streamlit as st
import pandas as pd
import main_functions
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# nltk.download("punkt")
# nltk.download("stopwords")

#Author: Andy Naranjo COP4813

# Get API Key
api_key_dic = main_functions.read_from_file("JSON_Files/api_key.json")
api_key = api_key_dic["my_key"]

# Intro body
st.title("COP 4813 - Web Application Programming")
st.title("Project - 1")
st.subheader("Part A - The Stories API")
st.write("This app uses the Top Stories API to display the most common words used in the top current articles based on a"
         " specified topic selected by the user. The data is displayed as a line chart and as a wordcloud image.")

# Creates and input field and the topic options select box
st.subheader("I - Topic Selection")
userName = st.text_input(label="Please enter your name:",value='', max_chars=None, key=None, type='default')
topicInt = st.selectbox(
    "Select a topic of your interest",
    ["","arts", "automobiles", "books", "business", "fashion", "food", "health", "home", "insider", "magazine", "movies",
     "nyregion", "obituaries", "opinion", "politics", "realestate", "science", "sports", "sundayreview", "technology",
     "theater", "t-magazine", "travel", "upshot", "us", "and world"]
    )
# Makes sure that the name has greater than a letter and that an topic is selected
if len(userName) > 1 and len(topicInt) > 0:
    #  User feedback of the selection of options
    st.write("Hi " + userName.title() + ", you selected the " + topicInt.title() + " topic.")

    # Creates the url and file for the top stories
    url_top = "https://api.nytimes.com/svc/topstories/v2/" + topicInt + ".json?api-key=" + api_key
    response = requests.get(url_top).json()
    main_functions.save_to_file(response,"JSON_Files/top_stories.json")
    top_articles = main_functions.read_from_file("JSON_Files/top_stories.json")
    # Gets a string with all the text in the abstract of all topics and the 10 most used words
    top_art_abst = main_functions.allAbstWords(top_articles)
    top_article_words = main_functions.topWords(top_art_abst,10)

    # Creates the plot chart
    st.subheader("II - Frequency Distribution")
    if st.checkbox("Click here to generate frequency distribution"):

        pos_x = [x[0] for x in top_article_words]
        pos_y = [y[1] for y in top_article_words]

        top_words = pd.DataFrame({
            'Words': pos_x,
            'Count' : pos_y
        })
        top_words = top_words.rename(columns={'Words': 'index'}).set_index('index')
        st.line_chart(top_words)
    # Creates the wordcloud using all the words in abstract from the articles of the selected topic
    st.subheader("III - Wordcloud")
    if st.checkbox("Click here to generate wordcloud"):

        wordcloud_top = WordCloud().generate(top_art_abst)
        image_top= plt.figure(figsize=(12, 12))
        plt.imshow(wordcloud_top)
        plt.axis("off")
        plt.show()
        st.pyplot(image_top)
        st.text("Wordcloud created for the top articles in the " + topicInt.title() + " topic.")

# Part B Body
st.subheader("Part B - Most Popular Articles")
st.write("Select if you want to see the most shared, emailed or viewed articles.")

# Creates the select box for the preferred article and period of time
preferredArt = st.selectbox(
    "Select your preferred set of articles",
    ["","shared","emailed","viewed"]
)

periodTime = st.selectbox(
    "Select the period of time (last days)",
    ["",1,7,30]
)

# Checks that both select box were selected
if len(preferredArt) > 0 and len(str(periodTime)) > 0:
    # Creates the url and file for the most popular stories
    url_most_pop = "https://api.nytimes.com/svc/mostpopular/v2/" + preferredArt + "/" + str(periodTime)+".json?api-key=" + api_key
    response = requests.get(url_most_pop).json()
    main_functions.save_to_file(response, "JSON_Files/most_pop_stories.json")
    pop_articles = main_functions.read_from_file("JSON_Files/most_pop_stories.json")
    # Gets a string with all the text in the abstract of all topics
    pop_art_abst = main_functions.allAbstWords(pop_articles)

    # Creates the wordcloud using all the words in abstract from the articles of the selected topic
    wordcloud_pop = WordCloud().generate(pop_art_abst)
    image_pop = plt.figure(figsize=(12, 12))
    plt.imshow(wordcloud_pop)
    plt.axis("off")
    plt.show()
    st.pyplot(image_pop)
    st.text("Wordcloud created for the most " + preferredArt.title() + " articles in the last " + str(periodTime) + " days")