import numpy as np
from tqdm import tqdm
from gensim import corpora, models

from get_windows import get_windows
import glob
from collections import Counter

MIN_COUNTS = 20
MAX_COUNTS = 1800
MIN_LENGTH = 15
HALF_WINDOW_SIZE = 5

files = glob.glob("../segmented/*.txt")
encoder = dict() # word -> id
texts = []
word_idx = 0
for i, file in enumerate(files):
    text = []
    with open(file) as fstream:
        for line in fstream:
            word = line.strip()
            
            if word not in encoder:       # build a dict of all words
                encoder[word] = word_idx
                word_idx += 1

            text.append(word)
    texts.append((i, text))


print("Unique words in texts:", word_idx)

decoder = {word:i for i, word in encoder.items()}

encoded_docs = []
for i, text in texts:
    encoded_docs.append(list(map(lambda x: encoder[x], text)))

data = []

for index, doc in enumerate(encoded_docs):
    windows = get_windows(doc, HALF_WINDOW_SIZE)
    data += [[index, w[0]] + w[1] for w in windows]


all_texts = []
for i, text in texts:
    all_texts.extend(text)

cnt = Counter(all_texts)
word_counts = np.zeros(max(decoder.keys()) + 1)
for i, word in decoder.items():
    word_counts[i] = cnt[word]

unigram_distribution = word_counts/sum(word_counts)

data = np.array(data, dtype='int64')

np.save('decoder.npy', decoder)
np.save('data.npy', data)
np.save('unigram_distribution.npy', unigram_distribution)