import sentiment_mod as s

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


print(s.sentiment("This movie was awesome! The acting was great, plot was wonderful, and there were pythons...so yea!"))
print(s.sentiment("This is crap, junk, horrible, fuck.."))
print(s.sentiment("Today kinda sux! But I'll get by, lol"))
print(s.sentiment("Asshole!!! u r so mean"))
