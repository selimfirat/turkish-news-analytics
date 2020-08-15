#!/usr/bin/env python
# -*- coding: latin-1 -*-
import nltk.data
from nltk import wordpunct_tokenize
from nltk.tokenize import WordPunctTokenizer

class Tokenizer:

    def __init__(self):
        self._sentence_tokenizer = nltk.data.load("./tokenizer/punkt_turkish.pickle")
        self.word_tokenizer = WordPunctTokenizer()
        abbreviations = set()
        with open("./tokenizer/abbreviations-long.txt") as f:
            for l in f:
                abbreviations.add(l.split(':')[0])

        self._sentence_tokenizer._params.abbrev_types = abbreviations


    def sentences_from_text(self, text):
        return self._sentence_tokenizer.tokenize(text.strip()),


    def tokens_from_sentence(self, sentence):
        return nltk.word_tokenize(sentence)