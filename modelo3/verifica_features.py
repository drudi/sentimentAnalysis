#! /usr/bin/env python

import pickle
import nltk
import string

palavras = pickle.load(open("palavras-frequentes.p", "rb"))
palavras = set(palavras)


def get_words(texto):
    words = [w.lower()
             for w in nltk.word_tokenize(texto)
             if w not in string.punctuation]
    return set(words)


def busca_features(words):
    found_features = [w
                      for w in words
                      if w in palavras]
    return found_features


def mostra_palavras_frequentes(texto):
    words = get_words(texto)
    print "As seguintes palavras estão entre as 850 mais frequentes: ",
    for word in busca_features(words):
        print "\"%s\"," % word,

    print "\n"
