# Alan Perez
# AXP200075

# ou will create bigram and unigram dictionaries for English, French, and Italian
# using the provided training data where the key is the unigram or bigram text and the value is the
# count of that unigram or bigram in the data. Then for the test data, calculate probabilities for
# each language and compare against the true labels.

import pathlib
import pickle

from nltk import word_tokenize
from nltk.util import ngrams


def read_file(filepath):
    # with open(pathlib.Path.cwd().joinpath(filepath), 'r') as f:
    #     text_in = f.read()

    read_text = open(pathlib.Path.cwd().joinpath(filepath), 'r', encoding='utf-8')
    text_in = read_text.read()

    text_in = text_in.replace("\n", "")

    tokens = word_tokenize(text_in)

    # using nltk to create a bigram list
    bigrams = list(ngrams(tokens, 2))
    # using nltk to create a ngram list
    # unigrams = ngrams(tokens, 1)

    # use the bigram list to create a bigram dictionary of bigrams and counts,
    # [‘token1 token2’] -> count
    # use the unigram list to create a unigram dictionary of unigrams and counts,
    # [‘token’] -> count
    unigrams_dict = {t: tokens.count(t) for t in set(tokens)}
    bigrams_dict = {b: bigrams.count(b) for b in set(bigrams)}


    return unigrams_dict, bigrams_dict


if __name__ == '__main__':
    # English pickle
    unigrams_dict_english,bigrams_dict_english = read_file('data/LangId.train.English')
    pickle.dump(unigrams_dict_english, open('LangID.Unigrams.English.p', 'wb'))
    pickle.dump(bigrams_dict_english, open('LangID.Bigrams.English.p', 'wb'))


    # French Pickle
    unigrams_dict_french,bigrams_dict_french = read_file('data/LangId.train.French')
    pickle.dump(unigrams_dict_french, open('LangID.Unigrams.French.p', 'wb'))
    pickle.dump(bigrams_dict_french, open('LangID.Bigrams.French.p', 'wb'))


    # Italian Pickle
    unigrams_dict_italian,bigrams_dict_italian = read_file('data/LangId.train.Italian')
    pickle.dump(unigrams_dict_italian, open('LangID.Unigrams.Italian.p', 'wb'))
    pickle.dump(bigrams_dict_italian, open('LangID.Bigrams.Italian.p', 'wb'))
