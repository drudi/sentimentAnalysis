#! /usr/bin/env python
# _*_ coding: utf-8 _*_
"""
Exemplo de um classificador Naive Bayes.

Exemplo de um classificador Naive Bayes utlizando
os recursos da NLTK.

"""

import nltk
import sys
#from pprint import pprint
from nltk.corpus import movie_reviews
import random

documents = [(list(movie_reviews.words(fileid)), category)
             for category in movie_reviews.categories()
             for fileid in movie_reviews.fileids(category)]
random.shuffle(documents)

all_words = nltk.FreqDist(w.lower()
                          for w in movie_reviews.words())
word_features = all_words.keys()[:2000]


def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        features['contains(%s)' % word] = (word in document_words)
    return features

#print document_features(movie_reviews.words('pos/cv957_8737.txt'))

featuresets = [(document_features(d), c) for (d, c) in documents]
train_set, test_set = featuresets[100:], featuresets[:100]
classifier = nltk.NaiveBayesClassifier.train(train_set)

print nltk.classify.accuracy(classifier, test_set)

print classifier.show_most_informative_features(5)

#print classifier.classify()

sys.exit(0)
