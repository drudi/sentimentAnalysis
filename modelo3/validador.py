#! /usr/bin/env python
# _*_ coding: utf-8 _*_
"""
Treina um classificador Naive Bayes e classifica comentarios.

Le dados de um corpus customizado, treina um classificador e
fornece estatisticas do classificador treinado.

"""
import nltk
from nltk.corpus import LazyCorpusLoader
from nltk.corpus import CategorizedPlaintextCorpusReader
import random
#import mysql.connector
import sys
import string
#import enchant

stopwords = nltk.corpus.stopwords.words('portuguese')


def document_features(document):
    document_words = set(document)
    features = {}
    for word in word_features:
        if word not in stopwords and word not in string.punctuation:
            features['contains(%s)' % word] = (word in document_words)
    return features

## Inicio do Treinamento
catho = LazyCorpusLoader(
    'catho_treinamentoV2', CategorizedPlaintextCorpusReader,
    r'(?!\.).*\.txt', cat_pattern=r'(negativo|positivo|neutro)/.*')

print "Preparando documentos para treinamento..."
sys.stdout.flush()
documents = [(list(catho.words(fileid)), category)
             for category in catho.categories()
             for fileid in catho.fileids(category)]
print "fim da preparacao dos documentos de treinamento."
sys.stdout.flush()

## Pre-processamento
corpus_words = [w.lower()
                for w in catho.words()
                if w not in string.punctuation]

random.shuffle(documents)

all_words = nltk.FreqDist(corpus_words)

word_features = all_words.keys()[:850]

#print word_features
#sys.exit(1)

featuresets = [(document_features(d), c)
               for (d, c) in documents]

train_set, test_set = featuresets[:500], featuresets[500:]

print 'Iniciando treinamento ...',
classifier = nltk.NaiveBayesClassifier.train(train_set)
print 'fim'
## Fim do treinamento.

## Analise

print 'Precisão: ', nltk.classify.accuracy(classifier, test_set)


neutro = 0
positivo = 0
negativo = 0
for comment in test_set:
    features, classe = comment[0], comment[1]
    classificado = classifier.classify(features)
    print '---------------------------'
    #print comment[0]
    print 'classe -->> ', comment[1]
    print 'classificado -->> ', classificado
    if classificado == 'neutro':
        neutro += 1
    elif classificado == 'positivo':
        positivo += 1
    elif classificado == 'negativo':
        negativo += 1

print '---------------------------'
print ' Classificador -> Negativos: %s - Neutros: %s - Positivos: %s' % (negativo, neutro, positivo)
print 'Total: %s' % (negativo + neutro + positivo)

classifier.show_most_informative_features(20)

sys.exit(1)
## Classificacao jurado 1
print 'Validacao Jurado 1'

catho = LazyCorpusLoader(
    'catho', CategorizedPlaintextCorpusReader,
    r'(?!\.).*\.txt', cat_pattern=r'(negativo|positivo|neutro)/.*')

documentos = [(list(catho.words(fileid)), category)
              for category in catho.categories()
              for fileid in catho.fileids(category)]

featureset = [(document_features(d), c) for (d, c) in documentos]


print nltk.classify.accuracy(classifier, featureset)

classifier.show_most_informative_features(5)

## Classificacao jurado 2
print 'Classificacao jurado 2'

catho2 = LazyCorpusLoader(
    'catho2', CategorizedPlaintextCorpusReader,
    r'(?!\.).*\.txt', cat_pattern=r'(negativo|positivo|neutro)/.*')

documentos2 = [(list(catho2.words(fileid)), category)
               for category in catho2.categories()
               for fileid in catho2.fileids(category)]

featureset2 = [(document_features(d), c) for (d, c) in documentos2]


print nltk.classify.accuracy(classifier, featureset2)

classifier.show_most_informative_features(5)

## Classificacao jurado 3
print 'Classificacao jurado 3'

catho3 = LazyCorpusLoader(
    'catho3', CategorizedPlaintextCorpusReader,
    r'(?!\.).*\.txt', cat_pattern=r'(negativo|positivo|neutro)/.*')

documentos3 = [(list(catho3.words(fileid)), category)
               for category in catho3.categories()
               for fileid in catho3.fileids(category)]

featureset3 = [(document_features(d), c) for (d, c) in documentos3]


print nltk.classify.accuracy(classifier, featureset3)

classifier.show_most_informative_features(5)

# Classificacao jurado 4
print 'Classificacao jurado 4'

catho4 = LazyCorpusLoader(
    'catho4', CategorizedPlaintextCorpusReader,
    r'(?!\.).*\.txt', cat_pattern=r'(negativo|positivo|neutro)/.*')

documentos4 = [(list(catho4.words(fileid)), category)
               for category in catho4.categories()
               for fileid in catho4.fileids(category)]

featureset4 = [(document_features(d), c) for (d, c) in documentos4]


print nltk.classify.accuracy(classifier, featureset4)

classifier.show_most_informative_features(5)

## Classificacao jurado 5

catho5 = LazyCorpusLoader(
    'catho5', CategorizedPlaintextCorpusReader,
    r'(?!\.).*\.txt', cat_pattern=r'(negativo|positivo|neutro)/.*')

documentos5 = [(list(catho5.words(fileid)), category)
               for category in catho5.categories()
               for fileid in catho5.fileids(category)]

featureset5 = [(document_features(d), c) for (d, c) in documentos5]


print nltk.classify.accuracy(classifier, featureset5)

classifier.show_most_informative_features(5)

#######################################################
## Grava o resultado da classificacao em banco de dados

# conn = mysql.connector.connect(user='root',
#                                host='127.0.0.1',
#                                database='modelo3')

# conn2 = mysql.connector.connect(user='root',
#                                 host='127.0.0.1',
#                                 database='modelo3')


# cursor = conn.cursor()
# cursor2 = conn2.cursor()
# select = """SELECT id_comentario, comentario_usuario
#                 FROM resultado_classificacao
#                 WHERE classe IS NULL"""
# cursor.execute(select)

# print("Tentando fazer o trabalho")
# print cursor
# for (idc, comm) in cursor:
#     print '.',
#     sys.stdout.flush()
#     words = [w.lower()
# #             for w in nltk.word_tokenize(comm.encode('utf-8'))
#              for w in nltk.word_tokenize(comm)
#              if w not in string.punctuation]
#              #if w not in string.punctuation and
#              #w not in stopwords]

#     #words = spell_check(words)
#     classe = classifier.classify(document_features(words))
#     update = """UPDATE resultado_classificacao
#                     SET classe = '%s'
#                     WHERE id_comentario = %s""" % (classe, idc)
#     cursor2.execute(update)
#     cursor2.execute('COMMIT')
