#! /usr/bin/env python
# _*_ coding: utf-8 _*_

from selenium import webdriver
import time
import mysql.connector

browser = webdriver.Firefox()

browser.get('http://translate.google.com/#pt/en/')
source = browser.find_element_by_id('source')
result_box = browser.find_element_by_id('result_box')
gt_clear = browser.find_element_by_id('gt-clear')
gt_submit = browser.find_element_by_id('gt-submit')

conn1 = mysql.connector.connect(user='root',
                                host='127.0.0.1',
                                database='analise')
conn2 = mysql.connector.connect(user='root',
                                host='127.0.0.1',
                                database='analise')
cursor1 = conn1.cursor()
cursor2 = conn2.cursor()

select = """SELECT id_comentario, comentario_usuario
            FROM analise.comentarios_traduzidos
            WHERE comentario_traduzido IS NULL"""
cursor1.execute(select)

for idc, comentario in cursor1:
    source.send_keys(comentario)
    gt_submit.click()
    time.sleep(1.5)
    comentario_traduzido = result_box.text
    if comentario_traduzido == '':
        print 'Erro ao traduzir. Tentando novamente.'
        time.sleep(5.0)
        comentario_traduzido = result_box.text
    if comentario_traduzido == '':
        print 'Erro ao traduzir. Desistindo...'
    else:
        update = """UPDATE analise.comentarios_traduzidos
                    SET comentario_traduzido = %s
                    WHERE id_comentario = %s"""

        cursor2.execute(update, (comentario_traduzido, idc,))
        #print cursor2.statement
        cursor2.execute('COMMIT')
    gt_clear.click()


browser.quit()
