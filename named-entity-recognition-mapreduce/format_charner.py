import numpy as np
from keras.utils.np_utils import to_categorical

from preprocess import WordPreprocessor
from preprocess import prepare_preprocessor, WordPreprocessor

class FormatCharNER:

    def __init__(self, train_file=None, test_file=None, validation_file=None, sentence_max_length=250):
        self.chars = ["_PAD_", "_UNK_"]
        self.sentence_max_length = sentence_max_length

        self.train_x, self.train_y, self.test_x, self.test_y, self.val_x, self.val_y = None, None, None, None, None, None

        self.labels = set()
        self.chars = {"_PAD_", "_UNK_"}

        all_sentences, all_labels = self.get_data("./data/all.txt")
        self.pp = prepare_preprocessor(all_sentences, all_labels)
        self.num_chars = len(self.pp.vocab_word)
        self.num_labels = len(self.pp.vocab_tag)


        if train_file:
            self.get_data(train_file)

        if validation_file:
            self.get_data(validation_file)

        if test_file:
            self.get_data(test_file)
        print(self.labels)

        self.label_i = { lbl: i for i, lbl in enumerate(self.labels) }
        self.i_label = { i: lbl for i, lbl in enumerate(self.labels) }

        self.i_char = { i: chr for i, chr in enumerate(self.chars) }
        self.char_i = { chr: i for i, chr in enumerate(self.chars) }

        if train_file:
            self.train_x, self.train_y = self.get_x_y(train_file)

        if test_file:
            self.test_x, self.test_y = self.get_x_y(test_file)

        if validation_file:
            self.val_x, self.val_y = self.get_x_y(validation_file)





    def get_data(self, path_file):
        sentences = []
        lbls = []
        with open(path_file, encoding="utf-8") as file:
            sentence_words = []
            sentence_labels = []
            for l in file:
                l = l.replace("\n", "")
                self.chars |= set(l)
                if l != "":
                    word, label = l.split("\t")
                    sentence_words.append(word)
                    sentence_labels.append(label)
                    self.labels |= set([ label ])
                else:
                    sentences.append(sentence_words)
                    lbls.append(sentence_labels)
                    sentence_words = []
                    sentence_labels = []

        return np.asarray(sentences), np.asarray(lbls) ###


    def get_x_y(self, file_path):

        sentences, labels = self.get_data(file_path)
        res = self.pp.transform(sentences, labels)
        print(0, np.asarray(res[0][0]).shape)
        print(1, np.asarray(res[0][1]).shape)
        print()
        return res[0][0], res[1]

    def char_to_i(self, chr):

        i = self.char_i[chr] if chr in self.char_i else self.char_i["_UNK_"]

        return i

    def label_to_i(self, label):
        return self.label_i[label]


    def sentence_to_x(self, sentence):
        r = np.zeros(self.sentence_max_length)
        for i, chr in enumerate(sentence[:self.sentence_max_length]):
            r[i] = self.char_to_i(chr)

        return r.reshape((-1, self.sentence_max_length))