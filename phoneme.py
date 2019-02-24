import nltk

pd = nltk.corpus.cmudict.dict()

with open("english-words/words_alpha.txt") as f:
    words = f.read().strip().splitlines()

yes = 0
no = 0
for word in words:
    try:
        pd[word]
        yes += 1
    except KeyError:
        no += 1

print(f"Yes: {yes}; No: {no}")
