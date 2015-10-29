#! /usr/bin/env python
# _*_ coding: utf-8 _*_
"""Modulo para testar a classe SentiFinder."""

import unittest
from sentifinder import SentiFinder
from sentilex import Sentilex


class SentiFinderTestCase(unittest.TestCase):

    """Testa o SentimentFinder. """

    def setUp(self):
        print "Iniciando teste"
        self.sf = SentiFinder(Sentilex('../SentiLex-PT02'))

    def test_is_instance(self):
        self.assertIsInstance(self.sf, SentiFinder)

    def test_sentence_tokenization(self):
        texto = "Importante. Para mim infelizmente não funcionou, "
        texto += "mas conheço pessoas que deu muito certo a inscrição"
        texto += " e está trabalhando."
        self.assertIsInstance(self.sf.sent_tokenize(texto), list)
        self.assertEquals(len(self.sf.sent_tokenize(texto)), 2)

    def test_word_tokenization(self):
        texto = "O rato, roeu a roupa. Do rei de roma."
        esperado = ['o', 'rato', 'roeu', 'a', 'roupa', 'do', 'rei',
                    'de', 'roma']
        self.assertEquals(self.sf.word_tokenize(texto), esperado)

    def test_text_tokenization(self):
        texto = "Importante. Para mim infelizmente não funcionou, "
        texto += "mas conheço pessoas que deu muito certo a inscrição"
        texto += " e está trabalhando."
        esperado = [['importante'],
                    ['para', 'mim', 'infelizmente', 'não', 'funcionou', 'mas',
                     'conheço', 'pessoas', 'que', 'deu', 'muito', 'certo', 'a',
                     'inscrição', 'e', 'está', 'trabalhando']]
        self.assertEquals(self.sf.text_tokenizer(texto), esperado)

    def test_stopword_removal(self):
        texto = "Vamos ao castelo. Pois a noite é nossa."
        esperado = [['vamos', 'castelo'],
                    ['pois', 'noite', 'é', 'nossa']]
        tokenizado = self.sf.text_tokenizer(texto)
        self.assertEquals(self.sf.remove_stopwords(tokenizado), esperado)

    def test_sentiment_score(self):
        texto = "O site é bom. E o visual é bonito."
        texto += " Mas a usabilidade é péssima."
        esperado = 1
        processado = self.sf.remove_stopwords(self.sf.text_tokenizer(texto))
        self.assertEquals(self.sf.get_score(processado), esperado)

    def test_sentimento_negativo(self):
        texto = "Não gostei. O site não me ajudou."
        processado = self.sf.remove_stopwords(self.sf.text_tokenizer(texto))
        self.assertLess(self.sf.get_score(processado), 0)

    def test_sentimento_positivo(self):
        texto = "Gostei bastante. O site me ajudou a encontrar um emprego"
        processado = self.sf.remove_stopwords(self.sf.text_tokenizer(texto))
        self.assertGreater(self.sf.get_score(processado), 0)

    def test_sentimento_neutro(self):
        texto = "Gostei do serviço. Mas o site é um lixo."
        processado = self.sf.remove_stopwords(self.sf.text_tokenizer(texto))
        self.assertEquals(self.sf.get_score(processado), 0)

    def testGetScoreFromUnprocessedText(self):
        texto = "Não gostei. O site não me ajudou."
        self.assertLess(self.sf.scoreFromText(texto), 0)

    def testClassifyText(self):
        texto = "Não gostei. O site não me ajudou."
        esperado = {'polaridade': 'negativo',
                    'score': -1}
        self.assertEquals(self.sf.classifyText(texto), esperado)

    def testSentimentoNegativo2(self):
        texto = "Muito caro!!!"
        esperado = {'polaridade': 'negativo',
                    'score': -1}
        self.assertEquals(self.sf.classifyText(texto), esperado)

    def testSentimentoNegativo3(self):
        texto = "Não é bom."
        esperado = {'polaridade': 'negativo',
                    'score': -1}
        self.assertEquals(self.sf.classifyText(texto), esperado)

    def testCorrectText(self):
        texto = "Umrato"
        processado = self.sf.remove_stopwords(self.sf.text_tokenizer(texto))
        esperado = [["um", "rato"]]
        self.assertEquals(self.sf.correctText(processado), esperado)

if __name__ == '__main__':
    unittest.main()
