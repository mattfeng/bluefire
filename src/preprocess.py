#!/usr/bin/env python

from gensim import corpora, models
from tqdm import tqdm
from collections import Counter
from lda2vec.get_windows import get_windows

import glob
import sys
import numpy as np

# define constants
MIN_COUNTS = 30
MAX_COUNTS = 250000
MIN_LENGTH = 15
HALF_WINDOW_SIZE = 5
N_TOPICS = 25

if len(sys.argv) != 2:
    print("Usage: ./preprocess <data folder>")
    quit()

data_folder = sys.argv[1]

# read in all the different documents
files = glob.glob(f"./data/{data_folder}/segmented/*.txt")
doc2id = dict()
id2doc = dict()
encoder = dict() # word -> id
encoded_docs = []
docs = []
word_idx = 0
for i, file in tqdm(enumerate(files)):
    doc2id[file] = i
    id2doc[i] = file
    encoded_doc = []
    doc = []
    with open(file) as fstream:
        for line in fstream:
            word = line.strip()
            
            if word not in encoder:          # build a dict of all words (the encoder)
                encoder[word] = word_idx
                word_idx += 1

            encoded_doc.append(encoder[word])
            doc.append(word)

    encoded_docs.append((i, encoded_doc))
    docs.append((i, doc))

print("Unique words in texts:", word_idx)

decoder = {i:word for word, i in encoder.items()}

# create a counter of all the words
all_words = []
for i, doc in docs:
    all_words.extend(doc)
    
counts = Counter(all_words)

word_counts = np.zeros(max(decoder.keys()) + 1)
for i, word in decoder.items():
    word_counts[i] = counts[word]

unigram_distribution = word_counts / sum(word_counts)

# create the windows for lda2vec to run over
data = []

print("[i] Generating windows...")
for index, doc in tqdm(encoded_docs):
    try:
        windows = get_windows(doc, HALF_WINDOW_SIZE)
        data += [[index, w[0]] + w[1] for w in windows]
    except AssertionError as e:
        print(str(e))
        print(id2doc[index])
        print(index)

data = np.array(data, dtype='int64')

# create the initial weights for the document vectors using raw LDA
texts = [list(filter(lambda w: MIN_COUNTS <= counts[w] <= MAX_COUNTS, doc)) for i, doc in docs]
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

print("[i] Forming LDA model...")
lda = models.LdaModel(corpus, alpha=0.9, id2word=dictionary, num_topics=N_TOPICS)
corpus_lda = lda[corpus]

# save the info needed to visualize in pyLDAvis
np.save(f"./data/{data_folder}/npy/LDA_lda.npy", lda)
np.save(f"./data/{data_folder}/npy/LDA_corpus.npy", corpus)
np.save(f"./data/{data_folder}/npy/LDA_dictionary.npy", dictionary)

# import pyLDAvis.gensim

# pyLDAvis.enable_notebook()
# pyLDAvis.gensim.prepare(lda, corpus, dictionary)

doc_weights_init = np.zeros((len(corpus_lda), N_TOPICS))

for i in tqdm(range(len(corpus_lda))):
    topics = corpus_lda[i]
    for j, prob in topics:
        doc_weights_init[i, j] = prob

# display the results of LDA
keywords = []
for i, topics in lda.show_topics(N_TOPICS, formatted=False):
    keywords.append(set([t for t, _ in topics]))
    print("topic", i, ":", " ".join([t for t, _ in topics]))

# save all the necessary data
np.save(f"./data/{data_folder}/npy/doc2id.npy", doc2id)
np.save(f"./data/{data_folder}/npy/id2doc.npy", id2doc)
np.save(f"./data/{data_folder}/npy/decoder.npy", decoder)
np.save(f"./data/{data_folder}/npy/unigram_distribution.npy", unigram_distribution)
np.save(f"./data/{data_folder}/npy/data.npy", data)
np.save(f"./data/{data_folder}/npy/doc_weights_init.npy", doc_weights_init)

# create the word vectors via a skip-gram word2vec model
vocab_size = len(decoder)
embedding_dim = 50

print("[i] Training word2vec model...")
# train a skip-gram word2vec model
texts = [doc for i, doc in docs]
model = models.Word2Vec(texts, size=embedding_dim, window=5, workers=4, sg=1, negative=15, iter=1000, min_count=1)
model.init_sims(replace=True)

word_vectors = np.zeros((vocab_size, embedding_dim)).astype('float32')
for word, i in encoder.items():
    word_vectors[i] = model.wv[word]

print("Number of word vectors:", len(model.wv.vocab))

# save the word2vec model
np.save(f"./data/{data_folder}/npy/word_vectors.npy", word_vectors)