from gensim.models import KeyedVectors

wv = KeyedVectors.load_word2vec_format("../supplementary/wordvec/chinese.vec", binary=False)
print(wv.most_similar(positive=""))
