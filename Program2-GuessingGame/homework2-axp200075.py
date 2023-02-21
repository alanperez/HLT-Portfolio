# Alan Perez
# axp200075
# Homework 2
# CS 4395.001

# This program is a guessing game where it reads the input file as raw text, calculate the lexical diversity of the tokenized text and output it,

import pathlib  # get current working dir
import sys  # to get system param

import nltk
from nltk import word_tokenize, pos_tag
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
import random


# read input file as raw text function
def preproccess(raw_text):
    """
        Preprocess raw text
        :param raw_text:
        :return: lexical diversity, tags,nouns

    """

    # calculate the lexical diversity
    # a. tokenize the lowercase raw text, reduce tokens that arent alpha, and have len > 5

    tokens4 = word_tokenize(raw_text)
    # lower case the text
    # tokens4 = [t.lower() for t in raw_text]
    # get rid of punctuation and stopwords
    tokens4 = [t.lower() for t in tokens4 if t.isalpha() and t not in stopwords.words('english') and len(t) > 5]
    # b. lemmatize the tokens and use set() to make a list of unique lemmas
    # get the lemmas
    wn1 = WordNetLemmatizer()
    #
    lemmas = [wn1.lemmatize(t) for t in tokens4]

    # make unqique
    lemmas_unique = set(lemmas)

    # c. do pos tagging on the unique set and print the first 20
    tags = pos_tag(lemmas_unique)
    # # calc lex diversity
    # print("\nLexical diversityL %.2f: " % (len(lemmas_unique)) / (len(tokens4)))
    print("The first 20 tagged: ", tags[:20])
    # d. create a list of only those lemmas that are nouns -> NN (noun)
    nouns_list = [x[0] for x in tags if x[1] == "NN"]

    print("# of Tokens: ", len(tokens4))
    print("# of Nouns: ", len(nouns_list))
    return tokens4, nouns_list


# Guessing Game Function

def guess_game(words):
    # a. give the user 5 points to start with; the game ends when their total score is negative, or they guess ‘!’ as a letter

    initial_score = 5

    # b. randomly choose one of the 50 words in the top 50 list (See the random numbers notebook in the Xtras folder of the GitHub)
    random_word = random.choice(words)

    # c. output to console an “underscore space” for each letter in the word
    hidden_words = '_' * len(random_word)
    print("Hidde Letters: ", hidden_words)

    # could use an empty string and append each guess, loop through check the index of the hidden word with string
    guessed_letters = ""

    while True:

        while initial_score > 0 or guessed_letters != "!":
            # d. ask the user for a letter, formatted to lower since our txt is formatted that way
            guessed_letter = input("Guess a letter: ").lower()

            # e. if the letter is in the word, print ‘Right!’, fill in all matching letter _ with the letter and add 1 point to their score
            if guessed_letter in random_word:

                # loop through the random word, if the char of random word is equal to the guessed letter, assign it to the index
                for i in range(len(random_word)):
                    if random_word[i] == guessed_letter:
                        # overwrite the _ with all the occurences of the correctly guessed letter, gets the before
                        hidden_words = hidden_words[:i] + guessed_letter + hidden_words[i + 1:]
                guessed_letters = guessed_letter
                initial_score += 1

                print("\nRight! Score is", initial_score)
                print(hidden_words)

            if random_word == hidden_words:
                print("You solved it!")
                print("current score: ", initial_score)
                print(hidden_words)
                break
            else:
                # f. if the letter is not in the word, subtract 1 from their score, print ‘Sorry, guess again
                initial_score -= 1
                print("Sorry, guess again")
                print("current score: ", initial_score)

            #   g. guessing for a word ends if the user guesses the word or has a negative scoreh. keep a cumulative total score and end the game if it is negative (or the user entered ‘!’) for a guess
            if guessed_letter == '!':
                print("the ! character was detected, will exit the game")
                initial_score -= 1
                break
            elif initial_score <= 0 or '!' in guessed_letters:
                print("\nG A M E O V E R")
                # reveal the word
                print("\n The word was: ", random_word)
                print("\nExiting..")
                break
        # i. right or wrong, give user feedback on their score for this word after each guess
        print("current score: ", initial_score)
        return initial_score


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please enter a filename as a system arg')

    rel_path = sys.argv[1]
    file_path = pathlib.Path.cwd().joinpath(rel_path)

    with open(file_path, 'r') as f:
        text_in = f.read()

    lex = word_tokenize(text_in)
    uniq = set(lex)
    # calc lex diversity
    print("\nLexical diversityL %.2f" % (len(uniq) / len(lex)))
    tokens, nouns = preproccess(text_in)

    # Make a dictionary of {noun:count of noun in tokens} items from the nouns and tokens lists;
    common_freq = {noun: tokens.count(noun) for noun in nouns}

    # sort the dict by count and print the 50 most common words and their counts. Save these words to a list because they will be used in the guessing game.

    # lambda func to sort by highest value first
    freq_words = sorted(common_freq.items(), key=lambda x: x[1], reverse=True)

    # save the 50 commons words
    common_words = []
    for i in range(50):
        common_words.append(freq_words[i][0])
    # prints the key and value of freq word
    print("\n50 most common words and count: ", freq_words)
    # save the 50 commons words
    # common = [x[0] for x in common_words[:50]]

    guess_game(common_words)
