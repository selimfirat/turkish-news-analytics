import pickle
import sys

from TurkishStemmer import TurkishStemmer
import math

import numpy as np

import argparse
import json as simplejson

import re
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, StandardOptions, SetupOptions
from apache_beam.metrics import Metrics
from apache_beam.metrics.metric import MetricsFilter
from apache_beam.io.textio import ReadFromText, WriteToText
import random
import nltk.data
import logging
from nltk.tokenize import WordPunctTokenizer
import re
import uuid
from apache_beam.pvalue import AsSingleton


def run():
    # Sentences From Text
    _sentence_tokenizer = nltk.data.load("./tokenizer/punkt_turkish.pickle")
    word_tokenizer = WordPunctTokenizer()
    abbreviations = set()
    with open("./tokenizer/abbreviations-long.txt") as f:
        for l in f:
            abbreviations.add(l.split(':')[0])

    _sentence_tokenizer._params.abbrev_types = abbreviations

    def sentences_from_text(text):
        return _sentence_tokenizer.tokenize(text.strip())

    def tokens_from_sentence(sentence):
        return sentence.split()  # nltk.word_tokenize(sentence)

    def ngrams(obj, n):
        tokens = []
        sentences = (
            sentences_from_text(obj["title"]) +
            sentences_from_text(obj["description"]) +
            sentences_from_text(obj["content"])
        )

        for sentence in sentences:
            tokens += tokens_from_sentence(sentence)

        pairs = nltk.ngrams(tokens, n)
        return [" ".join(pair) for pair in pairs]

    def convertToJsonObj(jsonText):
        return simplejson.loads(jsonText)

    def convertToObject(jsonObj):
        x = jsonObj

        obj = {
            "title": x.get("properties", {}).get("title", {}).get("stringValue", ""),
            "link": x.get("properties", {}).get("link", {}).get("stringValue", ""),
            "published": x.get("properties", {}).get("published", {}).get("stringValue", ""),
            "description": x.get("properties", {}).get("description", {}).get("stringValue", ""),
            "content": x.get("properties", {}).get("content", {}).get("stringValue", ""),
        }

        obj["key"] = obj["link"] if obj["link"] else str(uuid.uuid4())

        return obj

    # https://stackoverflow.com/questions/9662346/python-code-to-remove-html-tags-from-a-string
    def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    def removeHTMLFromStrings(obj):
        for key in obj.keys():
            obj[key] = cleanhtml(obj[key])

        return obj

    def tokenize_to_sentences(obj):

        obj["sentences"] = (
            sentences_from_text(obj["title"]) +
            sentences_from_text(obj["description"]) +
            sentences_from_text(obj["content"])
        )

        return obj

    def tokenize_to_words(obj):

        obj["tokens"] = []

        for sentence in obj["sentences"]:
            obj["tokens"] += tokens_from_sentence(sentence)

        for token in obj["tokens"]:
            yield (obj["key"], token)

    def get_named_entities(mdl, tokens):
        stemmer = TurkishStemmer()
        res = mdl.analyze(tokens)
        entities = []
        for entity in res["entities"]:
            for entity2 in entity["text"].split(", "):
                ne = stemmer.stem(entity2).split("'")[0]
                entities.append((entity["type"], ne, entity["score"]))
        return entities

    options = PipelineOptions()
    options.view_as(StandardOptions).runner = 'DirectRunner'

    p = beam.Pipeline(options=options)

    pairs = (p
             | "Read From Text" >> ReadFromText("news.json", coder=beam.coders.coders.StrUtf8Coder())  # line by line
             | "Convert to Json Object" >> beam.Map(convertToJsonObj)
             | "Convert to Python Object" >> beam.Map(convertToObject)
             | "Remove HTML Tags From Strings (Normalization 1)" >> beam.Map(removeHTMLFromStrings)
             )

    tokens_1gram = (pairs
                    | 'Sentence Tokenization' >> beam.Map(tokenize_to_sentences)
                    | 'Word Tokenization' >> beam.FlatMap(tokenize_to_words)  # also convert to key value pairs
                    )

    tokens = tokens_1gram

    def process_tokens_last(doc, tokens):
        return (doc, get_named_entities(tokens))

    doc_named_entities = (tokens
                          | beam.GroupByKey()
                          #     | beam.Map(lambda (doc, tokens): process_tokens_last(mdl, tokens))
                          )

    (doc_named_entities
     | "Write Results" >> WriteToText("doc_tokens")
     )

    p.run()


logging.getLogger().setLevel(logging.INFO)
run()