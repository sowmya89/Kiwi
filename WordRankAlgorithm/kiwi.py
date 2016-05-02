
import os
import sys
import re
import math
import collections
import itertools
import logging
import calendar, time
import string
import cPickle as pickle
from statistics import mode

import nltk, nltk.classify.util, nltk.metrics
from nltk.classify import NaiveBayesClassifier
from nltk.classify import ClassifierI
from nltk.classify.scikitlearn import SklearnClassifier
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.snowball import SnowballStemmer
from sklearn.naive_bayes import MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.svm import SVC, LinearSVC, NuSVC

from pyspark import SparkConf
from pyspark import SparkContext

from classifiers import generate_training_set, best_word_features_bi, get_all_dict
from util import gen_best_features, find_best_words

start_time = calendar.timegm(time.gmtime())

logging.basicConfig(filename='kiwi_log',level=logging.DEBUG)

# Module-level global variables for the `tokenize` function below
PUNCTUATION = set(string.punctuation)
STOPWORDS = set(stopwords.words('english'))
STEMMER = SnowballStemmer("english")
allowed_word_types = ["J","N","V","P","R"]
POLARITY_DATA_DIR = os.path.join('/Users/anil/', 'Kiwi')
RT_POLARITY_POS_FILE = os.path.join(POLARITY_DATA_DIR, 'pos_training.txt')
RT_POLARITY_NEG_FILE = os.path.join(POLARITY_DATA_DIR, 'neg_training.txt')

bad_words = []
with open('swearwords.txt','r') as bad:
	for line in bad:
		bad_words.append(line.strip())

TRAIN = False
TEST = False

stop_words = set(stopwords.words('english'))
sc = SparkContext('local', 'pyspark')

# this function takes a feature selection mechanism and returns its performance in a variety of metrics
def evaluate_features(sentence, best_words=[], posWords=[], negWords=[]):

	classifier_list = {}
	votes = []

	if TRAIN:
		# Generate Training Positive and Negative Set from Training Data.
		posFeatures, negFeatures = generate_training_set(best_word_features_bi, best_words, posWords, negWords)

		if TEST:
			#selects 3/4 of the features to be used for training and 1/4 to be used for testing
			posCutoff = int(math.floor(len(posFeatures)*3/4))
			negCutoff = int(math.floor(len(negFeatures)*1/4))
			trainFeatures = posFeatures[:posCutoff] + negFeatures[:negCutoff]
			testFeatures = posFeatures[posCutoff:] + negFeatures[negCutoff:]
		else:
			trainFeatures = posFeatures + negFeatures
			print "Training NaiveBayesClassifier Now"
			classifier = NaiveBayesClassifier.train(trainFeatures)
			pickle.dump(classifier, open("NaiveBayesClassifier.p", "wb"))
			classifier_list['NaiveBayesClassfier'] = classifier

			print "Training MNB_classifier Now"
			MNB_classifier = SklearnClassifier(MultinomialNB())
			classifier_list['MNB'] = MNB_classifier
			pickle.dump(classifier, open("MNB_classifier.p", "wb"))

			print "Training BernoulliNB Now"
			BernoulliNB_classifier = SklearnClassifier(BernoulliNB())
			classifier_list['BernoulliNB'] = BernoulliNB_classifier
			pickle.dump(classifier, open("BernoulliNB.p", "wb"))

			print "Training LogisticRegression Now"
			LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
			classifier_list['LogisticRegression'] = LogisticRegression_classifier
			pickle.dump(classifier, open("LogisticRegression.p", "wb"))

			print "Training LinearSVC Now"
			LinearSVC_classifier = SklearnClassifier(LinearSVC())
			classifier_list['LinearSVC'] = LinearSVC_classifier
			pickle.dump(classifier, open("LinearSVC.p", "wb"))

			# print "Training SGDClassifier Now"
			# SGDC_classifier = SklearnClassifier(SGDClassifier())
			# classifier_list['SGDClassifier'] = SGDC_classifier
			# pickle.dump(classifier, open("SGDClassifier.p", "wb"))

	else:

		classifier = pickle.load(open("NaiveBayesClassifier.p", "rb"))
		classifier_list['NaiveBayesClassfier'] = classifier

		classifier = pickle.load(open("MNB_classifier.p", "rb"))
		classifier_list['MNB_classifier'] = classifier

		classifier = pickle.load(open("BernoulliNB.p", "rb"))
		classifier_list['BernoulliNB'] = classifier

		classifier = pickle.load(open("LogisticRegression.p", "rb"))
		classifier_list['LogisticRegression'] = classifier

		classifier = pickle.load(open("LinearSVC.p", "rb"))
		classifier_list['LinearSVC'] = classifier

		# classifier = pickle.load(open("SGDClassifier.p", "rb"))
		# classifier_list['SGDClassifier'] = classifier

		#initiates referenceSets and testSets
	referenceSets = collections.defaultdict(set)
	testSets = collections.defaultdict(set)
	test_sentence = get_all_dict(sentence.split())

	for classifier, obj in classifier_list.iteritems():
		try:
			result = obj.classify(test_sentence)
			#print result
			votes.append(result)
		except:
			pass


	word_sentiment = mode(votes)
	total_sentiment = votes.count(word_sentiment)
	confidence_of_sentiment = total_sentiment / len(votes)

	#print "Word Sentiment = " + word_sentiment + " With Confidence = " + str(confidence_of_sentiment)
	return word_sentiment, confidence_of_sentiment


def evaluate_small_features(line):
	words = line.split()
	words = [word for word in words if word not in stop_words]
	for word in words:
		if word in bad_words:
			return "neg", 1
	else:
		return "pos", 1


# Function to break text into "tokens", lowercase them, remove punctuation and stopwords, and stem them
def tokenize(text):
	posWords= []
	tokens = word_tokenize(text)
	lowercased = [t.lower() for t in tokens]
	no_punctuation = []
	for word in lowercased:
	    punct_removed = ''.join([letter for letter in word if not letter in PUNCTUATION])
	    no_punctuation.append(punct_removed)
	stemmed = [STEMMER.stem(w) for w in no_punctuation]
	words = [w for w in stemmed if w]
	pos = nltk.pos_tag(words)
	for w in pos:
	    if w[1][0] in allowed_word_types:
	        posWords.append(w[0].lower())

	return posWords

def get_classifier():
	pos_file = sc.textFile(RT_POLARITY_POS_FILE)
	neg_file = sc.textFile(RT_POLARITY_NEG_FILE)

	pos_words = pos_file.map(lambda text: tokenize(text))
	neg_words = neg_file.map(lambda text: tokenize(text))
	return pos_words, neg_words


def get_sentiment(line):
	global TRAIN

	if TRAIN:
		print "Entering Training Mode"
		posWords,negWords = get_classifier()
		logging.debug("Dumping posWords and negWords to picke files")
		posWords = list(itertools.chain(*posWords.collect()))
		negWords = list(itertools.chain(*negWords.collect()))
		pickle.dump(posWords, open( "posWords.p", "wb" ))
		pickle.dump(negWords, open( "negWords.p", "wb" ))
		bigram_words = gen_best_features(posWords,negWords)
		pickle.dump(bigram_words, open("bigram_words.p", "wb"))
		best_words = find_best_words(bigram_words, 20000)
		pickle.dump(bigram_words, open("best_words.p", "wb"))
	else:
		logging.debug("Trying to Load Pickle Objects")
		posWords = pickle.load(open( "posWords.p", "rb" ))
		negWords = pickle.load(open( "negWords.p", "rb" ))
		bigram_words = pickle.load(open("bigram_words.p", "rb"))
		best_words = pickle.load(open("best_words.p", "rb"))

	if len(line.split()) <= 3:
			result, conf = evaluate_small_features(line)
			return result, conf
	else:
		result, conf = evaluate_features(line, best_words, posWords, negWords)
		TRAIN = False
		return result, conf

f = open('file_test.txt', 'r')
for line in f:
	print line
	result, conf = get_sentiment(line)
	print "Word Sentiment = " + result + " With Confidence = " + str(conf)
	print "\n"
f.close()
