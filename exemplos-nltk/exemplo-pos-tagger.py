#! /usr/bin/env python
# _*_ coding: utf-8 _*_
"""
Exemplo de um POS-tagger.

Exemplo de um POS-tagger para a lingua portuguesa utilizando
os recursos da NLTK.

"""

import nltk
import sys
from pprint import pprint
from nltk.corpus import floresta
#from nltk.corpus import mac_morpho


def simplify_tag(tg):
    if "+" in tg:
        return tg[tg.index("+") + 1:]
    else:
        return tg

# preprocessando as sentencas tageadas
tagged_sents = floresta.tagged_sents()
tagged_sents = [[(w.lower(), simplify_tag(t))
                 for (w, t) in sent] for sent in tagged_sents if sent]

# Conjunto de treinamento do tagger
train = tagged_sents[500:]

# Conjunto de testes do tagger
test = tagged_sents[:500]

print 'Conjunto de teste: %s' % len(test)
print 'Conjunto de treinamento: %s' % len(train)
# Descobre a tag mais comum no corpus e a utliza com o default tagger
tags = [simplify_tag(pos_tag) for (word, pos_tag)
        in floresta.tagged_words()]
most_freq_tag = nltk.FreqDist(tags).max()
tagger0 = nltk.DefaultTagger(most_freq_tag)

print "Tag mais frequente: %s" % most_freq_tag
print "Acuracia do tagger0 para ",
print " tag mais frequente: %s" % tagger0.evaluate(test)


# Tagger mais elaborado, construido em cima do default tagger
tagger1 = nltk.UnigramTagger(train, backoff=tagger0)
print "Acuracia do tagger1: %s" % tagger1.evaluate(test)

# Tagger mais elaborado ainda, construido em cima do tagger anterior
tagger2 = nltk.BigramTagger(train, backoff=tagger1)
print "Acuracia do tagger2: %s" % tagger2.evaluate(test)

tagger3 = nltk.TrigramTagger(train, backoff=tagger2)
print "Acuracia do tagger3: %s" % tagger3.evaluate(test)

frase = "Amanhã eu irei andar com uma"
frase += " moto excelente, e espero não levar nenhum tombo."
#frase = frase.decode('utf8').encode('ISO 8859-1')
print "Testando o tagger treinado com a seguinte frase: %s" % frase
print "Tagging: \n\n"
pprint(tagger2.tag(nltk.word_tokenize(frase.lower().
                                      decode('utf8').encode('latin1'))))
pprint(tagger2.tag(nltk.word_tokenize("não farei isso.".lower().
                                      decode('utf8').encode('latin1'))))

sys.exit(0)
