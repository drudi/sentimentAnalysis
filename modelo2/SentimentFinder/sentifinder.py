#! /usr/bin/env python
# _*_ coding: utf-8 _*_
# pylint: disable=R0201
"""Calculo de score de sentimento de comentarios."""

import nltk
import string
import enchant


class SentiFinder(object):

    """Calcula o score de sentimetos de textos."""

    # palavras a serem exluidas das stopwords
    not_stop_words = ['não', 'nossa']

    # palavras que indicam negacao de sentimento
    negation = ['não', 'nada', 'nunca']

    def __init__(self, sentilexInstance):
        self.sl = sentilexInstance

    def sent_tokenize(self, texto):
        """Tokeniza o comentario, devolvento uma lista."""

        sent_tok = nltk.data.load('tokenizers/punkt/portuguese.pickle')
        # pylint: disable=E1103
        return sent_tok.tokenize(texto)
        # pylint: enable=E1103

    def word_tokenize(self, sentence):
        """Tokeniza uma sentenca. Retornando uma lista."""

        # Remove pontuacao
        sent = ''.join([i.lower() for i in sentence
                        if i not in string.punctuation]).split(' ')
        # Sanitize the list
        for i, w in enumerate(sent):
            if len(w) == 0:
                sent.pop(i)
        return sent

    def text_tokenizer(self, texto):
        tokenized = []
        for sent in self.sent_tokenize(texto):
            tokenized.append(self.word_tokenize(sent))
        return tokenized

    def remove_stopwords(self, tokenized_text):
        stopwords = nltk.corpus.stopwords.words('portuguese')
        for word in self.not_stop_words:
            stopwords.remove(word)
        clean_text = []
        for line in tokenized_text:
            clean_line = [word for word in line if word not in stopwords]
            clean_text.append(clean_line)
        return clean_text

    def get_score(self, texto_processado):
        score = 0
        for sent in texto_processado:
            for i, word in enumerate(sent):
                flex = self.sl.searchFlex(word)
                if flex is not None:
                    if 'polaridade:n1' in flex.keys():
                        polaridade = flex['polaridade:n1']
                    else:
                        polaridade = flex['polaridade']
                    # Verifica se existe negacao e inverte o score
                    if i > 0 and sent[i - 1] in self.negation:
                        polaridade *= -1
                    elif i > 1 and sent[i - 2] in self.negation:
                        polaridade *= -1
                    print ("achou a flexão: %s com a polaridade %d" % (word, polaridade))
                    score += polaridade
        return score

    def scoreFromText(self, texto):
        processado = self.remove_stopwords(self.text_tokenizer(texto))
        corrigido = self.correctText(processado)
        return self.get_score(corrigido)

    def classifyText(self, texto):
        score = self.scoreFromText(texto)
        if score > 0:
            return {'polaridade': 'positivo',
                    'score': score}
        elif score < 0:
            return {'polaridade': 'negativo',
                    'score': score}
        else:
            return {'polaridade': 'neutro',
                    'score': score}

    def correctText(self, processado):
        dic = enchant.Dict('pt_BR')
        output = []
        for i, sent in enumerate(processado):
            output.append([])
            for word in sent:
                if len(word) > 0 and (not dic.check(word)):
                    sugestoes = dic.suggest(word)
                    if len(sugestoes) > 0:
                        for w in sugestoes[0].split():
                            output[i].append(w)
                else:
                    output[i].append(word)
        return output
