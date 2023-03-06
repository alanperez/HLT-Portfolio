import pickle
from nltk import word_tokenize
from nltk.util import ngrams


def calc_prob(text, unigram_dict, bigram_dict, V):
    # N is the number of tokens
    # V is the number of unique tokens, the vocabulary size

    # Each bigram’s probability with Laplace smoothing is: (b + 1) / (u + v) where b is
    # the bigram count, u is the unigram count of the first word in the bigram, and v is the total vocabulary size (add the lengths of the 3 unigram dictionaries).

    unigrams_test = word_tokenize(text)
    bigrams_test = list(ngrams(unigrams_test, 2))

    p_gt = 1
    p_laplace = 1
    p_log = 0  # somtimes prevents overflow

    for bigram in bigrams_test:
        n = bigram_dict[bigram] if bigram in bigram_dict else 0
        # n_gt = bigram_dict[bigram] if bigram in bigram_dict else 1 / N
        d = unigram_dict[bigram[0]] if bigram[0] in unigram_dict else 0
        # if d == 0:
        #     p_gt = p_gt * (1 / N)
        # else:
        #     p_gt = p_gt * (n_gt / d)
        p_laplace = p_laplace * ((n + 1) / (d + V))
        # p_log = p_log + math.log((n + 1) / (d + V))
        # print("\nprobability with simplified Good-Turing is %.5f" % (p_gt))
        # print("probability with laplace smoothing is %.5f" % p_laplace)
        # print("log prob is %.5f == %.5f" % (p_log, math.exp(p_log)))

    return p_laplace


if __name__ == '__main__':
    unigramEng = pickle.load(open('LangID.Unigrams.English.p', 'rb'))
    bigramEng = pickle.load(open('LangID.Bigrams.English.p', 'rb'))
    # loading french pickle
    unigramFR = pickle.load(open('LangID.Unigrams.French.p', 'rb'))
    bigramFR = pickle.load(open('LangID.Bigrams.French.p', 'rb'))
    # loading italian pickle
    unigramIT = pickle.load(open('LangID.Unigrams.Italian.p', 'rb'))
    bigramIT = pickle.load(open('LangID.Bigrams.Italian.p', 'rb'))

    # For each line in the test file, calculate a probability for each language (see note below) and
    # write the language with the highest probability to a file.
    test = open("data/LangId.test")
    read_test = test.readlines()

    # Holds the correct classifications
    solution = open("data/LangId.sol")
    read_solution = solution.readlines()
    output = open("output.txt", "w")
    correct = 0
    total = len(read_solution)
    V = len(unigramEng) + len(unigramFR) + len(unigramIT)
    # For each line in the test file, calculate a probability for each language (see note below) and
    # write the language with the highest probability to a file

    incorrect_lines = [];
    counter = 1

    for line in read_test:
        # prob of each lang
        eng_prob = calc_prob(line, unigramEng, bigramEng, len(unigramEng))
        print("English probability: ", eng_prob)
        fr_prob = calc_prob(line, unigramFR, bigramFR, len(unigramFR))
        print("French probability: ", fr_prob)
        it_prob = calc_prob(line, unigramIT, bigramIT, len(unigramIT))
        print("Italian probability: ", it_prob)

        if eng_prob >= fr_prob and eng_prob >= it_prob:
            lang = "English"
        elif fr_prob >= eng_prob and fr_prob >= it_prob:
            lang = "French"
        else:
            lang = "Italian"
        # write to file
        output.write(str(counter) + " " + lang + "\n")
        counter+=1
    test.close()
    output.close()

    with open('output.txt') as f:
        output = f.readlines()
    with open('data/LangId.sol') as f:
        read_solution = f.readlines()
    for i in range(len(read_solution)):
        if output[i] == read_solution[i]:
            correct += 1
        else:
            incorrect_lines.append(i + 1)
    print('Incorrect lines: ', incorrect_lines)
    accuracy = (correct / counter) * 100
    print(f"Accuracy: %2.f%%" % accuracy)
