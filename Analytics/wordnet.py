from nltk.corpus import wordnet

syns = wordnet.synsets("aloof")

#synset
print(syns[0].name())

#lemma just name
print(syns[0].lemmas()[0].name())

#definition of a word
print(syns[0].definition())

#display example for a word
print(syns[0].examples())

synonyms = []
antonyms = []

for syn in wordnet.synsets("dwarf"):
    for l in syn.lemmas():
        synonyms.append(l.name())
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())

print(set(synonyms))
print(set(antonyms))

w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('boat.n.01')
print(w1.wup_similarity(w2))

w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('car.n.01')
print(w1.wup_similarity(w2))

w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('cat.n.01')
print(w1.wup_similarity(w2))