from textblob import TextBlob
from nltk.tokenize import BlanklineTokenizer
from collections import Counter
import json
tokenizer = BlanklineTokenizer()
textwords  = open('C:\Users\Maithili\Desktop\Python wordcloud\sent.txt','r').read().split()
stopwords  = open('C:\Users\Maithili\Desktop\Python wordcloud\englishstop.txt','r').read().split()
markeredtext = []
filteredtext = [t for t in textwords if t.lower() not in stopwords]
cap_words = [word.upper() for word in filteredtext]
word_counts = Counter(cap_words)
word_counts
result = [{'key':key, 'value':value} for key,value in word_counts.items()]
with open('C:\Users\Maithili\Desktop\Python wordcloud\data.json', 'w') as outfile:
	json.dump(result,outfile,ensure_ascii=False)