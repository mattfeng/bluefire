#!/usr/bin/env python

import numpy as np
import sys

from lda2vec.train import train

def main():
    if len(sys.argv) != 2:
        print("Usage: ./main.py <data folder>")
        quit()

    data_folder = sys.argv[1]

    data = np.load(f"./data/{data_folder}/npy/data.npy")
    unigram_distribution = np.load(f"./data/{data_folder}/npy/unigram_distribution.npy")
    word_vectors = np.load(f"./data/{data_folder}/npy/word_vectors.npy")
    doc_weights_init = np.load(f"./data/{data_folder}/npy/doc_weights_init.npy")

    # transform to logits
    doc_weights_init = np.log(doc_weights_init + 1e-4)

    # make distribution softer
    temperature = 7.0
    doc_weights_init /= temperature

    # if you want to train the model like in the original paper
    # set doc_weights_init=None
    train(
        data, unigram_distribution, word_vectors,
        doc_weights_init=doc_weights_init,
        save_loc=f"./data/{data_folder}/models",
        n_topics=25,
        batch_size=1024*7, n_epochs=500,
        lambda_const=500.0, num_sampled=15,
        topics_weight_decay=1e-2,
        topics_lr=1e-3, doc_weights_lr=1e-3, word_vecs_lr=1e-3,
        save_every=5, grad_clip=5.0
    )


main()