# encoding=utf8
# -*- coding: utf-8 -*-

def run():
    import pickle
    import sys

    import math

    import numpy as np
    import apache_beam as beam

    reload(sys)
    sys.setdefaultencoding('utf8')

    import argparse
    import simplejson
    from gensim.models import KeyedVectors

    from apache_beam.options.pipeline_options import PipelineOptions, GoogleCloudOptions, StandardOptions, SetupOptions
    from apache_beam.io.textio import ReadFromText, WriteToText
    import nltk.data
    from nltk.tokenize import WordPunctTokenizer
    import re
    import uuid
    import perceptron
    # Sentences From Text
    _sentence_tokenizer = nltk.data.load("./tokenizer/punkt_turkish.pickle")
    word_tokenizer = WordPunctTokenizer()
    abbreviations = set()
    with open("./tokenizer/abbreviations-long.txt") as f:
        for l in f:
            abbreviations.add(l.split(':')[0])

    _sentence_tokenizer._params.abbrev_types = abbreviations

    model_file = "perceptron_word2vec_stemmed_normalized.pickle"
    with open(model_file, 'rb') as model:
        w, b = pickle.load(model)

    def sentences_from_text(text):
        return _sentence_tokenizer.tokenize(text.strip())

    def tokens_from_sentence(sentence):
        return nltk.word_tokenize(sentence)

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

    options = PipelineOptions()
    options.view_as(StandardOptions).runner = 'DirectRunner'

    p = beam.Pipeline(options=options)

    pairs = (p
             | "Read From Text" >> ReadFromText("news.json", coder=beam.coders.coders.StrUtf8Coder()) # line by line
             | "Convert to Json Object" >> beam.Map(convertToJsonObj)
             | "Convert to Python Object" >> beam.Map(convertToObject)
             | "Remove HTML Tags From Strings (Normalization 1)" >> beam.Map(removeHTMLFromStrings)
    )

    tokens_1gram = (pairs
            | 'Sentence Tokenization' >> beam.Map(tokenize_to_sentences)
            | 'Word Tokenization' >> beam.FlatMap(tokenize_to_words) # also convert to key value pairs
        )
    """
    tokens_2gram = (pairs
            | "Create 2-grams" >> beam.FlatMap(lambda obj: [(obj["key"], token) for token in ngrams(obj, 2)])
        )
    """

    tokens = tokens_1gram

    """
    vocabulary = (tokens
            | "Get words only" >> beam.Values()
            | "Remove duplicate words" >> beam.RemoveDuplicates()
        )
    vocabulary_size = (vocabulary
            | "Count Vocabulary elements" >> beam.combiners.Count.Globally()
        )

    doc_total_words = (tokens
            | "Count Words of Doc" >> beam.combiners.Count.PerKey()
    )
    """

    tokens_paired_with_1 = (tokens
            | "Pair with 1" >> beam.Map(lambda (doc, token): ((doc, token), 1))
    )
    """
    token_counts_per_doc = (tokens_paired_with_1
            | "Group by Doc,Word" >> beam.GroupByKey()
            | "Count ones" >> beam.Map(lambda ((doc, token), counts): (doc, (token, sum(counts))))
            | "Group by Doc" >> beam.GroupByKey()
        )



    num_docs = (token_counts_per_doc
            | "Get Docs" >> beam.Keys()
            | "Count Docs" >> beam.combiners.Count.Globally()
    )


    word_tf_pre = (
        { 'total_tokens': doc_total_words, 'token_counts_per_doc': token_counts_per_doc }
        | "CoGroup By Document" >> beam.CoGroupByKey()
    )

    def calc_tf((doc, count)):
        [token_count] = count['token_counts_per_doc']

        [tokens_total] = count['total_tokens']

        for token, cnt in token_count:
            yield token, (doc, float(cnt) / tokens_total)


    doc_word_tf = (word_tf_pre
        | "Compute Term Frequencies" >> beam.FlatMap(calc_tf)
        )

    word_occurrences = (tokens
        | "Remove Multiple occurrences per doc" >> beam.RemoveDuplicates()
        | "Pair with 1s" >> beam.Map(lambda (doc, word): (word, 1))
        | "Group by Word" >> beam.GroupByKey()
        | "Sum 1s" >> beam.Map(lambda (word, counts): (word, sum(counts)))
    )

    token_df = (
        word_occurrences
        | "Compute Document Frequency">> beam.Map(lambda (token, count), total: (token, float(count) / total), AsSingleton(num_docs)))

    token_tf_df = (
        { 'term_frequency': doc_word_tf, 'document_frequency': token_df}
        | "CoGroup By Token" >> beam.CoGroupByKey())

    def calc_tfidf((token, tfdf)):
      [df] = tfdf['document_frequency']
      for doc, tf in tfdf['term_frequency']:
        yield (doc, token), tf * math.log(1.0 / df)

    token_tf_idf = (token_tf_df
        | "Calculate TF-IDF Scores" >> beam.FlatMap(calc_tfidf)
    )
    """

    word2vec = KeyedVectors.load_word2vec_format('tr_word2vec', binary=True)

    def get_vec(word2vec, token):

        try:
            x = word2vec.get_vector(token)
            x = x.reshape(400)
        except:
            x = np.zeros(400)

        return x

    def analyze_sentiment(x):

        res = perceptron.f(x, w, b)

        return res

    doc_sentiment = (tokens_paired_with_1
                     | "Create Word2Vec Vector" >> beam.Map(lambda ((doc, token), cnt): (doc, get_vec(word2vec, token)))
                     | "Group Word2Vec Vectors By Document" >> beam.CombinePerKey(sum)
                     | "Sum Word2Vec Vectors" >> beam.Map(lambda (doc, vec): (doc, analyze_sentiment(vec)[0]))
                     )

    result = (doc_sentiment |
              "Format  Results" >> beam.Map(lambda (doc, tokens): '%s %s' % (doc, tokens))
              )

    (result
     | "Write Results" >> WriteToText("sentiments")
     )

    p.run()


if __name__ == '__main__':
    import timeit
    import logging

    start = timeit.timeit()
    logging.getLogger().setLevel(logging.INFO)
    run()
    end = timeit.timeit()
    print end - start
