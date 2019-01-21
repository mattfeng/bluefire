#!/usr/bin/env python

import logging
import pickle
import glob
from collections import OrderedDict

import numpy as np

from lda2vec import Corpus

logging.basicConfig()

SKIP_VAL = -2

vocab = OrderedDict() # word -> val
vocab["<SKIP>"] = SKIP_VAL

# 1. Load data into texts
# -----------------------
# texts is a 2D array, with each row representing
# a unique document, and each column in a row representing
# the word at that position.

files = glob.glob("../segmented/*.txt")
texts = []
word_idx = 0
for file in files:
    text = []
    with open(file) as fstream:
        for line in fstream:
            word = line.strip()
            
            if word not in vocab:       # build a dict of all words
                vocab[word] = word_idx
                word_idx += 1

            text.append(word)
    texts.append(text)

print("Unique words in texts:", word_idx)

# create token numpy array, with padding of non-characters with -2
max_length = max(len(text) for text in texts)
num_texts = len(texts)

tokens = np.full((num_texts, max_length), SKIP_VAL)

for row_idx, text in enumerate(texts):
    for col_idx, word in enumerate(text):
        tokens[row_idx, col_idx] = vocab[word]

corpus = Corpus()
# Make a ranked list of rare vs frequent words
corpus.update_word_count(tokens)
corpus.finalize()
# The tokenization uses spaCy indices, and so may have gaps
# between indices for words that aren't present in our dataset.
# This builds a new compact index
compact = corpus.to_compact(tokens)
# Remove extremely rare words
pruned = corpus.filter_count(compact, min_count=3)
# Convert the compactified arrays into bag of words arrays
bow = corpus.compact_to_bow(pruned)
# Words tend to have power law frequency, so selectively
# downsample the most prevalent words
clean = corpus.subsample_frequent(pruned)

# Now flatten a 2D array of document per row and word position
# per column to a 1D array of words. This will also remove skips
# and OoV words
doc_ids = np.arange(pruned.shape[0])
flattened, (doc_ids,) = corpus.compact_to_flat(pruned, doc_ids)
assert flattened.min() >= 0

# Fill in the pretrained word vectors
n_dim = 300
fn_wordvc = "../supplementary/wordvec/chinese.vec"
vectors, s, f = corpus.compact_word_vectors(vocab, filename=fn_wordvc)

# Save all of the preprocessed files
vocab_reversed = {v:k for k, v in vocab.items()}

pickle.dump(vocab_reversed, open("./bin/vocab.pkl", "wb"))
pickle.dump(corpus, open("./bin/corpus.pkl", "wb"))

np.save("./bin/flattened", flattened)
np.save("./bin/doc_ids", doc_ids)
np.save("./bin/pruned", pruned)
np.save("./bin/bow", bow)
np.save("./bin/vectors", vectors)