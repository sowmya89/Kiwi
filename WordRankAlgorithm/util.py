import logging
from nltk.probability import FreqDist, ConditionalFreqDist
from nltk.metrics import BigramAssocMeasures

logging.basicConfig(filename='kiwi.log',level=logging.DEBUG)


def find_best_words(word_scores, number):
    
    best_vals = sorted(word_scores.iteritems(), key=lambda (w, s): s, reverse=True)[:number]
    print best_vals[0:10]
    best_words = set([w for w, s in best_vals])
    return best_words

def gen_best_features(posWords, negWords):
   
    word_fd = FreqDist()
    cond_word_fd = ConditionalFreqDist()


    for word in posWords:
        word_fd.inc(word.lower())
        cond_word_fd['pos'].inc(word.lower())

    for word in negWords:
        word_fd.inc(word.lower())
        cond_word_fd['neg'].inc(word.lower())
 
 	pos_word_count = cond_word_fd['pos'].N()
    print "Positive Word Count = ", pos_word_count
    logging.debug("Positive Word Count = {0}".format(pos_word_count))

    neg_word_count = cond_word_fd['neg'].N()
    print "Negative Word Count = ", neg_word_count
    logging.debug("Negative Word Count = {0}".format(neg_word_count))

    total_word_count = pos_word_count + neg_word_count
    logging.debug("Total Word Count = {0}".format(total_word_count))
  
    #builds dictionary of word scores based on chi-squared test
    word_scores = {}
    for word, freq in word_fd.iteritems():
        pos_score = BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
        neg_score = BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count), total_word_count)
        word_scores[word] = pos_score + neg_score
  
    return word_scores