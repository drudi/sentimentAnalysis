#! /usr/bin/env python
# _*_ coding: utf-8 _*_
"""
Corpus Tagger.

Le dados em tabelas em um DB relacional (MySQL) , exibe
o comentario e pede por uma marcacao de positivo, negativo
ou neutro. Grava o resultado na tabela.

"""

import mysql.connector
#import os.path
import sys
from mysql2corpus import ComentarioReader


class MarcacaoWriter(object):

    """Grava uma marcacao do usuario no banco de dados."""

    def __init__(self,
                 user='root',
                 host='127.0.0.1',
                 database='modelo3'):
        self.conn = mysql.connector.connect(user=user,
                                            host=host,
                                            database=database)
        self.cursor = self.conn.cursor()

    def writeTag(self, tag, id_c):
        update = "UPDATE corpus_treinamento SET classe = '%s' where id_comentario = %s" % (tag, id_c)
        print update
        self.cursor.execute(update)
        self.cursor.execute('COMMIT')

    def askTags(self):
        q = """SELECT id_comentario, comentario_usuario
                FROM corpus_treinamento
                WHERE classe is NULL"""
        reader = ComentarioReader()
        reader.load_comentarios(query=q)
        corpus = reader.get_iterator()
        for id_comentario, comentario in corpus:
            #id_comentario, comentario = corpus.next()
            print '--------------------------'
            print 'id_comentario: %s' % id_comentario
            print 'comentario: %s' % comentario.encode('latin1').decode('latin1')
            print '--------------------------'
            userInput = raw_input("Entre 1 para positivo, 2 para negativo ou 3 para neutro. q para sair.")
            if userInput == '1':
                print 'positivo'
                tag = 'positivo'
            elif userInput == '2':
                print 'negativo'
                tag = 'negativo'
            elif userInput == '3':
                print 'neutro'
                tag = 'neutro'
            elif userInput == 'q':
                break
            else:
                print 'Deu merda. Fica pra proxima'
                break
            self.writeTag(tag, id_comentario)


if __name__ == '__main__':
    print 'Iniciando a coleta de marcacoes ...'
    marcador = MarcacaoWriter()
    marcador.askTags()

    sys.exit(1)
