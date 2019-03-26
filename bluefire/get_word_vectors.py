#!/usr/bin/env python

# Prepares the word vectors in the order specified from the preprocessing
# step in order initialize the lda2vec algorithm (speed up the results).

from gensim.models.keyedvectors import KeyedVectors
import numpy as np

embedding_dim = 300
data_folder = "AStockNewsV0"
encoder = np.load(f"./data/{data_folder}/npy/encoder.npy").item()
vocab_size = len(encoder)

# load word vectors
print(f"[i] Loading word vectors...")
CHINESE_WORDVEC_PATH = "../supplementary/wordvec/chinese.vec"
chinese_word_vectors = KeyedVectors.load_word2vec_format(CHINESE_WORDVEC_PATH, binary=False)

print(f"[i] Vocabulary size: {vocab_size}")
word_vectors = np.zeros((vocab_size, embedding_dim)).astype("float32")

for word, i in encoder.items():
    if i % 5000 == 0:
        print(f"[info] {i} words processed")
    if word in chinese_word_vectors:
        word_vectors[i] = chinese_word_vectors[word]
    else:
        print(f"[err] {word} not in chinese.vec, init to 0")

np.save(f"./data/{data_folder}/npy/word_vectors.npy", word_vectors)