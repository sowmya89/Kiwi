import cPickle as pickle
import os
import nltk

POLARITY_DATA_DIR = os.path.join('/home/nishanth/workspace/Sem4_finalProj/Kiwi/Webserver', 'data')
RT_POLARITY_POS_FILE = os.path.join(POLARITY_DATA_DIR, 'pos_training.txt')
RT_POLARITY_NEG_FILE = os.path.join(POLARITY_DATA_DIR, 'neg_training.txt')



import itertools
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

def bigram_word_feats(words, best_words):
    score_fn=BigramAssocMeasures.chi_sq
    n=500
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return dict([(ngram, True) for ngram in itertools.chain(words, bigrams)])

def best_word_features_bi(words, best_words):
    return dict([(word, True) for word in words if word in best_words])

def get_all_dict(words):
    return dict([(word, True) for word in words])

def generate_training_set(feature_select, best_words, posWords, negWords):
    posFeatures = []
    negFeatures = []

    with open(RT_POLARITY_POS_FILE, 'r') as posSentences:
        for line in posSentences:
            posWords = line.strip().split()
            posWords = [feature_select(posWords, best_words), 'pos']
            posFeatures.append(posWords)

    with open(RT_POLARITY_NEG_FILE, 'r') as negSentences:
        for line in negSentences:
            negWords = line.strip().split()
            negWords = [feature_select(negWords, best_words), 'neg']
            negFeatures.append(negWords)

    pickle.dump(posFeatures, open("posFeatures.p", "wb"))
    pickle.dump(posFeatures, open("negFeatures.p", "wb"))
    print "Done with generating training set"
    return posFeatures, negFeatures
