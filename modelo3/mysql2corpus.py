#! /usr/bin/env python
# _*_ coding: utf-8 _*_
"""
MySQL to corpus.

Le dados em tabelas em um DB relacional (MySQL) e monta um
corpus no mesmo formato do corpus movie_reviews da NLTK.

"""

import mysql.connector
import os.path
import sys


class Comentario(object):

    """
    Classe para representar um comentario.

    Contem os campos id_comentario, comentario_usuario, e polaridade.

    """

    def __init__(self,
                 id_comentario=None,
                 comentario_usuario=None,
                 polaridade=None):
        self.id_comentario = id_comentario
        self.comentario_usuario = comentario_usuario
        self.polaridade = polaridade

    def _tokenize_sents(self):
        pass

    def _tokenize_words(self):
        pass

    def _spellcheck(self):
        pass


class ComentarioReader(object):

    """Classe para ler comentarios do banco de dados."""

    def __init__(self,
                 user='root',
                 host='127.0.0.1',
                 database='modelo3'):
        self.conn = mysql.connector.connect(user=user,
                                            host=host,
                                            database=database)
        self.cursor = self.conn.cursor()

    def load_comentarios(self,
                         query='SELECT * FROM corpus_marcado5'
                         ):
        self.cursor.execute(query)

    def get_comentario(self):
        id_c, com, pol = self.cursor.next()
        return {'id_comentario': id_c,
                'comentario_usuario': com,
                'polaridade': pol}

    def get_iterator(self):
        return self.cursor


class CorpusWriter(object):

    """
    Classe para gravar comentarios como corpus.

    Esta classe grava os comentarios dos usuarios no formato do
    corpus movies_reviews.

    """

    def __init__(self,
                 user='root',
                 host='127.0.0.1',
                 database='modelo3',
                 dire='./catho'):
        self.reader = ComentarioReader(user=user,
                                       host=host,
                                       database=database)
        self.directory = dire

    def writeComment(self, id_comment, comment, polarity):
        filename = str(id_comment) + '.txt'
        comment = comment.encode('latin1')
        if polarity == 'positivo':
            filepath = self.directory + '/positivo/' + filename
        elif polarity == 'negativo':
            filepath = self.directory + '/negativo/' + filename
        else:
            filepath = self.directory + '/neutro/' + filename
        try:
            fp = open(os.path.normpath(filepath), 'wb')
            fp.write(comment)
            fp.close()
        except IOError as e:
            print 'Erro ao gravar arquivo: ', e.strerror
            print 'Arquivo: ', os.path.normpath(filepath)
            sys.exit(-1)

    def buildCorpus(self):
        self.reader.load_comentarios()
        for cId, comment, pol in self.reader.get_iterator():
            print '.',
            self.writeComment(cId, comment, pol)


if __name__ == '__main__':
    writer = CorpusWriter(dire='./catho5')
    #writer.writeComment('1', 'La la la la la la\n Rhrh sd dsf sdf slfjsdf\nAsdlfkslfk sldklsd fs', 'positivo')
    writer.buildCorpus()
