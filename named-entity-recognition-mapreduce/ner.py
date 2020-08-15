# -*- coding: utf-8 -*-
from unicode_tr import unicode_tr
from io import open
from TurkishStemmer import TurkishStemmer

from model_charner import ModelBiLSTM

model = ModelBiLSTM(dataset=None)

model.load_weights("model.h5")

def get_named_entities(model, tokens):
    stemmer = TurkishStemmer()
    res = model.analyze(tokens)
    entities = []
    for entity in res["entities"]:
        for entity2 in entity["text"].split(", "):
            ne = stemmer.stem(entity2).split("'")[0]
            entities.append((entity["type"], ne, entity["score"]))
    return entities



with open("doc_tokens-00000-of-00001", "r", encoding="utf-8") as ff:
    with open('doc_nes.txt', 'a+', encoding="utf-8") as target_file:
        nes = []
        for line in ff:
            link, tokens = eval(line)
            tokens = [unicode_tr(token) for token in tokens]
            target_file.write(unicode((link, get_named_entities(model, tokens))) + "\n")