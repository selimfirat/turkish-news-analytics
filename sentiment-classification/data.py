import os

import pickle

from sklearn.model_selection import train_test_split

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from tokenizer.tokenizer import Tokenizer
from normalizer import normalizer
from TurkishStemmer import TurkishStemmer
from gensim.models import KeyedVectors
import numpy as np

class Data:
    def _append_data(self, _type, normalized, stemmed):

        with open("data/" + _type + ("_normalized" if normalized else "") + ".txt", encoding="utf-8") as f:
            i = 0
            for s in f:
                self.x.append(self.stemmer.stem(s) if stemmed else s)
                self.y.append(str.upper(_type))
                if i == 1400:
                    break

    def __init__(self, normalized= True, classes= None, stemmed= True):
        if classes is None:
            classes = ["positive", "negative", "notr"]

        self.x = []
        self.y = []
        self.tokenizer = Tokenizer()
        self.stemmer = TurkishStemmer()
        self.word2vec = None

        self.cachefile = "data/data" + ("_normalized" if normalized else "") + ("_stemmed" if stemmed else "") + "_" + ("_".join(classes)) + ".pickle"
        if os.path.isfile(self.cachefile):
            with open(self.cachefile, 'rb') as cache:
                self.x, self.y = pickle.load(cache)
        else:
            for cls in classes:
                self._append_data(cls, normalized, stemmed)

            with open(self.cachefile, 'wb') as cache:
                pickle.dump((self.x, self.y), cache)


    def split(self, features):

        train_x, test_x, train_y, test_y = train_test_split(features, self.y, shuffle=True, test_size=0.2, random_state=1)

        return (train_x, train_y, test_x, test_y)


    def count_vectorized(self, ngram_range=(1,1)):
        vectorizer = CountVectorizer(analyzer="word", lowercase=False, ngram_range=ngram_range, tokenizer=self.tokenizer.tokens_from_sentence)

        features = vectorizer.fit_transform(self.x).toarray()

        return self.split(features)


    def tfidf_vectorized(self, ngram_range=(1,1)):
        vectorizer = TfidfVectorizer(analyzer="word", lowercase=False, ngram_range=ngram_range, tokenizer=self.tokenizer.tokens_from_sentence)

        features = vectorizer.fit_transform(self.x).toarray()

        return self.split(features)

    def word2vec_vectorized(self):
        if self.word2vec is None:
            self.word2vec = KeyedVectors.load_word2vec_format('tr_word2vec', binary=True)

        vecs = []
        for sentence in self.x:
            tokens = self.tokenizer.tokens_from_sentence(sentence)
            vec = np.zeros(400)
            for token in tokens:
                try:
                    vec += self.word2vec.get_vector(token)
                except:
                    pass
                    # print(token)

            vecs.append(vec)
        vecs = np.array(vecs)

        return self.split(vecs)