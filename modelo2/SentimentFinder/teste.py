#! /usr/bin/env python
# _*_ coding: utf-8 _*_

from sentilex import Sentilex

sl = Sentilex('../SentiLex-PT02')

frase = ['bom',
         'ruim',
         'avarento',
         'péssimo',
         'O',
         'rato',
         'roeu',
         'a',
         'roupa',
         'do',
         'rei',
         'de',
         'roma']
acumulador = 0
for palavra in frase:
    f = sl.searchFlex(palavra)
    if f is not None:
        acumulador += f['polaridade']

print 'Polaridade: ' + str(acumulador)
