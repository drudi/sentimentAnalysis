#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
Classifica comentarios armazenados em banco de dados.

Utiliza o sentifinder e o sentilex para classificar os
comentarios armazenados em banco de dados.

"""

import mysql.connector
from sentifinder import SentiFinder
from sentilex import Sentilex
import sys

db_config = {
    'user': 'root',
    'host': '127.0.0.1',
    'database': 'modelo2'
}

#####################################################################
sf = SentiFinder(Sentilex('../SentiLex-PT02'))
#####################################################################

conn = mysql.connector.connect(**db_config)
conn2 = mysql.connector.connect(**db_config)
cursor = conn.cursor()
cursor2 = conn2.cursor()

qry = """
SELECT id_comentario, comentario_usuario FROM comentarios;
"""
insert = ("""
INSERT INTO classificacao(id_comentario, classe, score)
VALUES(%s, %s, %s)
""")

cursor.execute(qry)

print '|',
for (id_comentario, comentario) in cursor:
    classificacao = sf.classifyText(comentario.encode('utf-8'))
    print '.',
    cursor2.execute(insert, (id_comentario,
                             classificacao['polaridade'],
                             classificacao['score']
                             ))
    cursor2.execute('COMMIT')
    sys.stdout.flush()
print '|'
