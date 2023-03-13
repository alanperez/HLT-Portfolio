# Alan Perez
# AXP200075
# CS4395.001
# Finding or Building a Corpus
import os.path

from bs4 import BeautifulSoup
import requests
import re

from nltk.tokenize import sent_tokenize, word_tokenize

from nltk.corpus import stopwords
import pickle


# web crawler function that starts with a URL representing a topic (a sport, your
# favorite film, a celebrity, a political issue, etc.) and outputs a list of at least 15 relevant
# URLs. The URLs can be pages within the original domain but should have a few outside
# the original domain.
def web_crawler(starter_url):
    # GET Request
    res = requests.get(starter_url)

    data = res.text

    soup = BeautifulSoup(data, 'html.parser')

    # Find all a tags
    links = soup.find_all('a')

    links_arr = []
    counter = 0
    for link in links:
        link_str = str(link.get('href'))
        if counter >= 15:
            break
        if '50cent' in link_str or '50 Cent' in link_str:
            if link_str.startswith('http') and 'google' not in link_str:
                links_arr.append(link_str)
                counter += 1
    print("links arr: ", links_arr)
    return links_arr


# function to loop through your URLs and scrape all text off each page. Store each
# page’s text in its own file
def scraper(links_arr):
    for link in links_arr:
        res = requests.get(link)
        data = res.text
        soup = BeautifulSoup(data, 'html.parser')
        text = soup.get_text()

        filename = link.split('/')[2] + '.txt'

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)


# function to clean up the text from each file

def clean_up():
    stop_words = set(stopwords.words('english'))

    text_files = [file for file in os.listdir('.') if os.path.isfile(file) and file.endswith('.txt')]

    for file in text_files:

        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()

        #       clean new lines , tabs
        text = text.replace('\n', ' ').replace('\t', ' ')

        # extract sentence using the tokenzier
        sentence_tok = sent_tokenize(text)

        # write to file

        new_file = os.path.splitext(file)[0] + 'NEW_CLEANED_UP.txt'

        with open(new_file, 'w', encoding='utf-8') as f:
            for sent in sentence_tok:
                f.write(sent + '\n')


# function to extract at least 25 important terms from the pages using an
# importance measure such as term frequency, or tf-idf.
def extract_top_terms():
    files = [file for file in os.listdir() if file.endswith('_cleaned_up.txt')]
    text = ""
    tf_dict = {}

    for file in files:
        with open(file, 'r') as f:
            text += f.read()
    tokens = word_tokenize(text.lower())
    tokens = [w for w in tokens if w.isalpha()
              and w not in stopwords.words('english')]
    # get term frequency
    for t in tokens:
        if t in tf_dict:
            tf_dict[t] += 1
        else:
            tf_dict[t] = 1

    # normalize tf by number of tokens
    for t in tf_dict.keys():
        tf_dict[t] = tf_dict[t] / len(tokens)

    # sorts and returns the highest freq term
    sort_tf = sorted(tf_dict.items(), key=lambda x: x[1], reverse=True)
    important_terms = [x[0] for x in sort_tf[:25]]



    manual_terms = ["50cent", "grodt", "love it", "rap", "hip-hop", "eminem", "dre", "gunit", "g-unit"]
    print("Terms: ", manual_terms)
    return manual_terms
# searchable knowledge base of facts that a chatbot (to be developed later) can
# share related to the 10 terms. The “knowledge base” can be as simple as a Python dict
# which you can pickle. More points for something more sophisticated like sql.
# def knowledge_bade():


if __name__ == '__main__':
    starter_url = "https://en.wikipedia.org/wiki/50_Cent"
    urls = web_crawler(starter_url)
    scraper(urls)
    clean_up()
    extract_top_terms()
