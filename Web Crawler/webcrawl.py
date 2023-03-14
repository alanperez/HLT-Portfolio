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
        link_href = str(link.get('href'))
        if counter == 15:
            break
        # strictly looking for music, but not enough links
        if '50 Cent' in link_href or '50cent' in link_href or 'Curtis James Jackson' in link_href or 'Curtis Jackson' in link_href or 'G-Unit' in link_href or 'Get Rich or Die Tryin' in link_href:
            if link_href.startswith('http') and 'google' not in link_href:
                links_arr.append(link_href)
                counter += 1

    # print("links arr: ", links_arr)

    for link in links_arr:
        print({link})
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
    text_files = [file for file in os.listdir('.') if os.path.isfile(file) and file.endswith('.txt')]

    for file in text_files:

        with open(file, 'r', encoding='utf-8') as f:
            text = f.read()

        #       clean new lines , tabs
        text = text.replace('\n', ' ').replace('\t', ' ')

        # extract sentence using the tokenzier
        sentence_tok = sent_tokenize(text)

        # write to file

        new_file = os.path.splitext(file)[0] + '_NEW_CLEANED_UP.txt'

        with open(new_file, 'w', encoding='utf-8') as f:
            for sent in sentence_tok:
                f.write(sent + '\n')


# function to extract at least 25 important terms from the pages using an
# importance measure such as term frequency, or tf-idf.
def extract_top_terms():
    files = [file for file in os.listdir() if file.endswith('_NEW_CLEANED_UP.txt')]

    tf_dict = {}

    for file in files:
        text = ""
        with open(file, 'r', encoding='utf-8') as f:
            text += f.read()
            # print("printing read text: " + text)
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

        # sorts and returns the highest freq term, first 25, could retreive 25 to 40 but this work
        sort_tf = sorted(tf_dict.items(), key=lambda x: x[1], reverse=True)
        important_terms = [sort_tf[:24]]
        print(important_terms)
        manual_terms = ['50 cent', 'massacre', 'g unit', 'hook', 'club', 'released', 'record', 'stone', 'albums',
                        'tryin']
        print("Selected top 10 terms: ", manual_terms)


def knowledge_base():
    kb = {
        "50 cent": "Curtis James Jackson III (born July 6, 1975), known professionally as 50 Cent, is an American rapper, actor, television producer, and businessman.",
        "massacre": "The Massacre is the second studio album by American rapper 50 Cent.",
        "g unit": "G-Unit (short for Guerilla Unit) was an American hip hop group formed by longtime friends and East Coast rappers 50 Cent, Tony Yayo, and Lloyd Banks.",
        "hook": "A hook is a musical idea, often a short riff, passage, or phrase, that is used in popular music to make a song appealing and to catch the ear of the listener.",
        "club": "an association or organization dedicated to a particular interest or activity.",
        "released": "allow or enable to escape from confinement; set free.",
        "record": "a thing constituting a piece of evidence about the past, especially an account kept in writing or some other permanent form.",
        "albums": "a collection of recordings issued as a single item on CD, record, or another medium.",
        "get rich or die tryin": "Get Rich or Die Tryin' is the debut studio album by American rapper 50 Cent. It was released on February 6, 2003, by Interscope Records, Dr. Dre's Aftermath Entertainment, Eminem's Shady Records, and 50 Cent's G-Unit Records"
    }

    # save the pickle file
    pickle.dump(kb, open('knowledge_base.p', 'wb'))  # write binary
    with open('knowledge_base.p', 'rb') as f:
        kb_pickle = pickle.load(f)

    for key, val in kb_pickle.items():
        print("Knowledge Base: ", key + ":" + val)


if __name__ == '__main__':
    starter_url = "https://en.wikipedia.org/wiki/50_Cent"
    urls = web_crawler(starter_url)
    scraper(urls)
    clean_up()
    extract_top_terms()

    # searchable knowledge base of facts that a chatbot (to be developed later) can
    # share related to the 10 terms. The “knowledge base” can be as simple as a Python dict
    # which you can pickle. More points for something more sophisticated like sql.

    knowledge_base()
