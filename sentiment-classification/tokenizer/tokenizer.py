#!/usr/bin/env python
# -*- coding: latin-1 -*-
import nltk.data
from nltk import wordpunct_tokenize
from nltk.tokenize import WordPunctTokenizer

class Tokenizer:

    def __init__(self):
        self.word_tokenizer = WordPunctTokenizer()


    def tokens_from_sentence(self, sentence):
        return nltk.word_tokenize(sentence)