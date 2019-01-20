#!/usr/bin/env python

import jieba
import jieba.posseg as pseg
import glob
import string
import re

def load_doc(path):
    """Load in a document"""
    corpus = ""
    with open(path) as f:
        for line in f:
            corpus += re.sub(r"\s+", "", line).strip()
    return corpus

def segment(doc):
    """Segment the document"""
    seg_list = jieba.cut(doc, cut_all=False)
    return seg_list

def load_stop_words():
    """Load stopwords into a set"""
    stopwords = set()
    stopfiles = glob.glob("../supplementary/stopwords/*")
    for stop in stopfiles:
        with open(stop) as f:
            for line in f:
                stopwords.add(line.strip())

    return stopwords

def isnt_stop_word(word, stopwords):
    """Helper function to determine if something is a stopword"""
    if word in stopwords:
        return False
    
    ascii_ = set(string.printable + "“”")
    if any((c in ascii_) for c in word):
        return False
    
    return True

def filter_stop_words(lst, stopwords):
    """Remove stopwords from a list of words"""
    return list(filter(lambda x: isnt_stop_word(x, stopwords), lst))

def get_pos(doc):
    words = pseg.cut(doc)
    return words

def get_proper_nouns(doc):
    tags = get_pos(doc)
    proper_nouns = set()
    for word, flag in tags:
        if flag in {"nr", "ns", "nt", "nz"}:
            proper_nouns.add(word)
    return proper_nouns

def filter_proper_nouns(words, nouns):
    return list(filter(lambda x: x not in nouns, words))

def process_file(path, stopwords):
    doc = load_doc(path)
    seg_list = segment(doc)
    filtered = filter_stop_words(seg_list, stopwords)

    proper_nouns = get_proper_nouns(doc)
    filtered = filter_proper_nouns(filtered, proper_nouns)

    # Remove proper nouns?
    # Preliminary solution: remove words that appear infrequently

    return filtered

def main():
    stopwords = load_stop_words()

    files = glob.glob("../extracted/*.txt")
    files = ["../extracted/20190114071928_3101.txt"]
    files = ["../extracted/20190115005958_3103.txt"]
    for path in files:
        doc = load_doc(path)

        processed = process_file(path, stopwords)
        for word in processed:
            print(word)


if __name__ == "__main__":
    main()