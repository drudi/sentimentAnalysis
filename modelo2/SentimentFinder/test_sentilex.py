#! /usr/bin/env python
# _*_ coding: utf-8 _*_

import unittest
from sentilex import Sentilex
import os


class SentilexTestCase(unittest.TestCase):

    """Testes para a classe Sentilex."""

    def setUp(self):
        self.sl = Sentilex('../SentiLex-PT02')

    def test_sentilex_dir_exists(self):
        """Verifica se o diretorio do Sentilex existe."""
        sentilex_dir_path = self.sl.getSentilexDir()
        self.assertTrue(os.path.isdir(sentilex_dir_path),
                        msg='sentilex_dir_path: {}'.format(sentilex_dir_path))

    def test_lemas_exists(self):
        """Verifica se o arquivo de lemas do sentilex existe."""

        lemas_path = self.sl.getLemasPath()
        self.assertTrue(os.path.isfile(lemas_path),
                        msg='lemas_path: {}'.format(lemas_path))

    def test_flex_exists(self):
        """Verifica se o arquivo de flexoes existe."""

        flex_path = self.sl.getFlexPath()
        self.assertTrue(os.path.isfile(flex_path),
                        msg='flex_path: {}'.format(flex_path))

    def test_linha_lema_eh_valida(self):
        """Verifica validade de linha do arquivo de lemas."""

        linha = self.sl.getLemaLine()
        self.assertEquals(linha.count(';'), 3,
                          msg='linha.count(\';\')-> {}'.format(linha.count(';')
                                                               ))

    def test_lema_eh_valido(self):
        """Testa se o lema retornado na estrutura eh uma palavra."""

        lema = self.sl.getLema()
        self.assertIsInstance(lema['lema'], str)

    def test_polaridade_negativa(self):
        """Testa se a polaridade do lema eh negativa."""

        lema = self.sl.getLema()
        self.assertEquals(lema['polaridade'], 1)

    def test_lemas_diferentes(self):
        """Testa se existem lemas diferentes sento retornados."""

        lema1 = self.sl.getLema()
        lema2 = self.sl.getLema(10)
        self.assertNotEqual(lema1['lema'], lema2['lema'])

    def test_busca_lema_ruim(self):
        """Testa se consegue achar o lema."""

        lema = self.sl.searchLema('ruim')
        self.assertEquals(lema['lema'], 'ruim')
        self.assertEquals(lema['polaridade'], -1)

    def test_busca_dois_lemas(self):
        """Testa se consegue achar dois lemas diferentes."""

        lema1 = self.sl.searchLema('ruim')
        lema2 = self.sl.searchLema('bom')
        self.assertEquals(lema1['lema'], 'ruim')
        self.assertEquals(lema1['polaridade'], -1)
        self.assertEquals(lema2['lema'], 'bom')
        self.assertEquals(lema2['polaridade'], 1)

    def test_busca_lema_inexistente(self):
        """Testa o comportamento de se buscar um lema inexistente."""

        lema = self.sl.searchLema('sadsdfasdfasdfasdfasdfasdfasfd')
        self.assertIsNone(lema)

    def test_linha_flex_eh_valida(self):
        """Testa se a linha de uma flexao eh valida."""

        linha = self.sl.getFlexLine()
        isInFaixa = linha.count(';') in (4, 5)
        self.assertTrue(isInFaixa,
                        msg='linha.count(\';\')-> {}'.format(linha.count(';')))

    def test_flex_eh_valido(self):
        """Testa se a flexao eh valida."""

        flexao = self.sl.getFlex()
        self.assertIsInstance(flexao['flex'], str)

    def test_flex_polaridade_positiva(self):
        """Testa se a polaridade da flexao eh positiva."""

        flexao = self.sl.getFlex()
        self.assertEquals(flexao['polaridade'], 1)

    def test_busca_flex_pessimo(self):
        """Testa se consegue buscar a flexao péssimo"""

        flexao = self.sl.searchFlex('péssimo')
        self.assertEquals(flexao['flex'], 'péssimo')
        self.assertEquals(flexao['polaridade'], -1)

    def test_busca_duas_flexoes(self):
        """Testa a busca de duas flexoes diferentes"""

        flexao1 = self.sl.searchFlex('ruim')
        flexao2 = self.sl.searchFlex('excelente')
        self.assertEquals(flexao1['flex'], 'ruim')
        self.assertEquals(flexao1['polaridade'], -1)
        self.assertEquals(flexao2['flex'], 'excelente')
        self.assertEquals(flexao2['polaridade'], 1)


if __name__ == '__main__':
    unittest.main()
