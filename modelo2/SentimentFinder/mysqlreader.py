#! /usr/bin/env python
# _*_ coding: utf-8 _*_
"""
Reader para disponibilizar um corpus via MySQL.

Classe para disponibilizar uma tabela do mysql como um corpus
na NLTK.

"""

import mysql.connector
from nltk.data import LazyLoader
from nltk.tokenize import TreebankWordTokenizer
from nltk.util import AbstractLazySequence, LazyMap, LazyConcatenation


class MySQLDBLazySequence(AbstractLazySequence):
    def __init__(self, host='127.0.0.1', user='root', database='modelo3',
                 table='corpus_marcado', column='comentario_usuario'):
        self.conn = mysql.connector.connect(user=user, host=host, database=database)
        self.table = table
        self.column = column

    def __len__(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(1) FROM %s' % self.table)
        leng, = cursor.next()
        return leng
