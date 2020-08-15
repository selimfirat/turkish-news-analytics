# Turkish News Analytics

Anaconda environment is used to ease the setup of the environment. Without anaconda, python gives lots of errors while the setup of packages.

Anaconda/Conda can be downloaded from here: https://conda.io/docs/user-guide/install/download.html

Re-used codes are stated inside the section of particular program.

* All you need is to execute the commands in-order in shell on root folder after the installing environments.

* You do not need to do anything else, hopefully :). https://media.giphy.com/media/F7yLXA5fJ5sLC/giphy.gif

![](https://www.cipher-it.co.uk/wp-content/uploads/2017/11/ITCrow.jpg)

This is very probable that pip gives errors. In case of any failures, please tell us via e-mail.

* This file is in Markdown format. Can be viewed in style via http://markdownlivepreview.com/.


## General Installation
```
conda create -n turkish_news_analytics python=2.7
conda create -n turkish_news_analytics_py35 python=3.5
```
Both python 3.5 and python 2.7 are used.

## Breadth First Crawler
```
conda activate turkish_news_analytics_py35
cd bf-crawler
pip install -r requirements.txt
scrapy crawl news -a target="https://www.takvim.com.tr/"
```

* It gives error unless running on Google Cloud Compute instance with Google Cloud Datastore access.
* However, even the error demonstrates that it scrapes the text from takvim.com.tr
* Implemented by Selim Fırat Yılmaz

## Latest News Crawler
```
conda activate turkish_news_analytics_py35
cd latest-news-crawler
pip install -r requirements.txt
python main.py
```
* Scrapes RSSs every 15 minutes. First crawling start after 15 minutes than program started
* It gives error unless running on Google Cloud Compute instance with Google Cloud Datastore access.
* However, even the error demonstrates that it scrapes the data from RSSs.
* Implemented by Selim Fırat Yılmaz

## Bloom Filtering Notebook (Experiment)
```
conda activate turkish_news_analytics_py35
cd bloom-filtering
pip install -r requirements.txt
python main.py
```
* Then, open the notebook via shown URL on the console.
* Implemented by Selim Fırat Yılmaz

## LSH First Trial (To study, not included in the report)
```
conda activate turkish_news_analytics_py35
cd lsh-first-trial
wget https://github.com/selimfirat/bilkent-turkish-writings-dataset/blob/master/data/texts.csv
pip install -r requirements.txt
jupyter notebook
```
* Initial purpose was to cluster the similar news and infer accordingly by sentiment scores and
* Then, open the notebook via shown URL on the console.
* However, this folder is not included in final report or presentation of our project.
* Only added because the project description says that "you should demonstrate how much effort you put into this project".
* Instead of wget, you can just download the url to that folder.
* Implemented by Selim Fırat Yılmaz

## Sentiment Classification

```
conda activate turkish_news_analytics_py35
cd sentiment-classification
pip install -r requirements.txt
jupyter notebook
```
* Normalizer is adopted from https://github.com/uozcan12/Twitter-Data-Normalization
* Pre-trained sentence tokenizer model is downloaded from https://www.kaggle.com/nltkdata/punkt and combined with zemberek's abbreviations-long corpus https://github.com/ahmetaa/zemberek-nlp/blob/master/tokenization/src/main/resources/tokenization/abbreviations-long.txt
* Stemmer is from https://github.com/otuncelli/turkish-stemmer-python
* Labeled 6k tweets dataset is from https://github.com/sercankulcu/twitterdata
* Pre-trained Word2Vec model is at https://github.com/akoksal/Turkish-Word2Vec
* Our experiments (with sklearn) are at logistic_regression.ipynb, naive_bayes.ipynb, nearest_centroid.ipynb, perceptron.ipynb, svm.ipynb and sgd.ipynb.
* The logistic regression(perceptron) algorithm we implemented is at perceptron.py and perceptron.ipynb files.
* Implemented by Selim Fırat Yılmaz

## Sentiment Classification via MapReduce
```
conda activate turkish_news_analytics
cd sentiment-classification-mapreduce
pip install -r requirements.txt
python main.py
```
* Pre-trained sentence tokenizer model is downloaded from https://www.kaggle.com/nltkdata/punkt and combined with zemberek's abbreviations-long corpus https://github.com/ahmetaa/zemberek-nlp/blob/master/tokenization/src/main/resources/tokenization/abbreviations-long.txt
* Pre-trained Word2Vec model is at https://github.com/akoksal/Turkish-Word2Vec
* The logistic regression(perceptron) algorithm we implemented is at perceptron.py and pickle version for easy use is at  perceptron_word2vec_stemmed_normalized.pickle
* Results are in "sentiments-00000-of-00001" file.
* Initialization might be slow since pre-trained word2vec model is taken to the memory.
* Implemented by Selim Fırat Yılmaz

## Named Entity Recognition
```
conda activate turkish_news_analytics
cd named-entity-recognition-mapreduce
pip install -r requirements.txt
python main.py
python ner.py
```

* F1 Score calculation is taken from https://github.com/Hironsan/anago/blob/master/anago/metrics.py and https://medium.com/@thongonary/how-to-compute-f1-score-for-each-epoch-in-keras-a1acd17715a2
* Preprocessing data(model/preprocessing.py) file according to ConLL standards and converting them to one_hot vector format to be trained via Keras is done via a file that is taken from https://github.com/Hironsan/anago/blob/master/anago/preprocess.py
* To convert softmax results back to the matrices, tagger.py from https://github.com/Hironsan/anago/blob/master/anago/tagger.py is used.
* This code re-uses these things, however, implements similar model to Kuru et al. 's state-of-art Turkish Named Entity Recognition model instead of anago's model with CRF(Viterbi decoder) model [1].
* Training history is at training_history.txt. This training is limited with 2 due to time constraints. Original training to create the model we show is early stopped at 9th epoch.

* Resulting (doc, named_entities) tuples are in [./named-entity-recognition-mapreduce/doc_nes.txt](./named-entity-recognition-mapreduce/doc_nes.txt).

* Implemented by Selim Fırat Yılmaz

## Combine Sentiments with Named Entities via Mapreduce
```
conda activate turkish_news_analytics
cd combine-sentiments-nes
pip install -r requirements.txt
python combine_sentiments_nes.py
```

* Results are in "ne_sentiment.txt-00000-of-00001" file to be indexed by elasticsearch.
* Implemented by Selim Fırat Yılmaz

## LSH - ApacheBeam

* Both of LSH executable have hardcoded hash functions and band numbers. If you want, you can change from code.

*	corpus_lsh.py is the python file that we have tested our lsh Apache Beam
    implementation on corpusdataset.txt the result of this python file is
    "outcorpus" run as : python corpus_lsh.py

    to get more information about corpus dataset go to = https://ir.shef.ac.uk/cloughie/resources/plagiarism_corpus.html#Download
    corpus-final09.xls has the categories of the plagiarised homeworks
    cut means copy and paste(start and end points are not same),
    light means slightly revisioned version of original homework(high similarity)
    heavy means heavily revisioned version of original homework  (low similarity)
    non means it is an original homework(almost non siimilarity)

    to evaluate the lsh run checklshout.py and get evaluation output printed on terminal




*	news_lsh.py is the python file that we have tested our lsh Apache Beam
    implementation on our own news dataset which is news.json,
    the result of this python file is "outnews"
    (	note: this can take up to 14 minutes as news.json is 300 MB but we get clusters of similar news as output :D )
    (
        note2: pairwise result of the pipeline is commented out because it takes
        3 hours and 15 gb ram to show pairwise output - you can test if you want to.
        Output of 14 minute run is the cluster of similar news so it works fine
    )
    run as : python news_lsh.py

* Files are under /lsh folder.

* Implemented by Berk Mandıracıoğlu

* You should copy news.json from root folder to /lsh folder if you want to run.


## Kibana For Dataset and Results Visualization

* to create a cluster and get elasticsearch and kibana endpoints go to = https://www.elastic.co/cloud


* once you create a cluster you will receive password , kibana_endpoint, and elsaticsearch_endpoint like ours as belows:
    username: elastic
    pasword : JFSEs3GIGmuB5W0VZNGyFJPy

    kibana: https://934b84c4c59ac5f737fcb609076603d8.us-east-1.aws.found.io:9243

    elastic: https://ffc97d66cc49d80123c71f8d348824e1.us-east-1.aws.found.io:9243
* then run :
    *news_kibana.py to convert news.json to elastice and get news_kibana output
    *doc_sentiment_kibana.py to convert doc_sentiment.txt to elasticsearch and get doc_sentiment output
    *nes.py to convert ne_sentiment.txt to elastic search and get LOC,ORG,PER outputs
* then upload these outputs to elastic search as:
    * curl -u elastic -H 'Content-Type: application/x-ndjson' -XPOST 'https://ffc97d66cc49d80123c71f8d348824e1.us-east-1.aws.found.io:9243/_bulk' --data-binary @PER

* we are ready to visualize in kibana at endpoint = https://934b84c4c59ac5f737fcb609076603d8.us-east-1.aws.found.io:9243

* Files are under /kibana folder.

* You should copy news.json from root folder to /kibana folder if you want to run.

* Implemented by Berk Mandıracıoğlu

## Experimenting on Full Crawled Dataset
If you want to run Mapreduce jobs on full dataset, you just need to copy-paste news.json on root folder to the folder to be ran.

## References
[1] Kuru, O., Can, O. A., & Yuret, D. (2016). Charner: Character-level named entity recognition. In Proceedings of COLING 2016, the 26th International Conference on Computational Linguistics: Technical Papers (pp. 911-921).

## Group Members
* Selim Fırat Yılmaz
* Berk Mandıracıoğlu