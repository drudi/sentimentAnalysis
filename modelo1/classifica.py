#! /usr/bin/env python
# _*_ coding: utf-8 _*_

import mysql.connector
from selenium import webdriver
import requests
import time
#import sys
import json
#from pprint import pprint
#from repustate import Repustate


APIKEY = '866491bfc461e4a329f9fabddcad713c95ef1915'

# Necessario inicializar o browser antes
browser = webdriver.Firefox()
browser.get('https://www.repustate.com/api-demo/')
browser.find_element_by_xpath('//*[@id="id_api_call"]/option[2]').click()


class Score(object):
    def __init__(self, id_comentario, score):
        self.id = id_comentario
        self.score = score

    def setId(self, id_comentario):
        self.id = id_comentario

    def setScore(self, score):
        self.score = score

    def getId(self):
        return self.id

    def getScore(self):
        return self.score


def getScoreFromRepustate(comentario):
    input = browser.find_element_by_id('id_text')
    input.clear()
    time.sleep(0.2)
    input.send_keys(comentario)
    time.sleep(0.5)
    submit_btn = browser.find_element_by_id('submit')
    submit_btn.click()
    output = browser.find_element_by_xpath('//*[@id="wrap"]/div[2]/div/div[1]/form/div[2]/pre')
    retorno = json.loads(output.text)
    if retorno['status'] == 'OK':
        return retorno['score']
    else:
        raise Exception('Retorno do JSON nao foi OK')


def updateNewScore(score):
    conn = mysql.connector.connect(host='127.0.0.1', user='root', db='analise')
    cursor = conn.cursor()
    updateSql = """UPDATE scores_selenium
                SET score = %s
                WHERE id_comentario = %s"""
    cursor.execute(updateSql, (score.getScore(), score.getId(),))
    cursor.execute('COMMIT')
    conn.close()


# Modificar a funcao processaLote para
# funcionar com somente um elemento.
def processaLote(lote):
    # montagem dos parametros
    paramsPost = {}
    for item in lote:
        texto_chave = 'text' + str(item['id_comentario'])
        texto_valor = item['comentario_traduzido']
        paramsPost[texto_chave] = texto_valor

    # Chamada a API do Repustate
    r = requests.post(
        'http://api.repustate.com/v2/' + APIKEY + '/bulk-score.json', data=paramsPost
    )
    data = r.json()

    # Insere no banco
    conn = mysql.connector.connect(host='127.0.0.1', user='root', db='analise')
    cur = conn.cursor()
    resultados = data['results']
    for item in resultados:
        sql = """INSERT INTO scores_atuais(id_comentario, score)
                 VALUES(%s, '%f')""" % (item['id'], item['score'])
        cur.execute(sql)
        cur.execute('COMMIT')
    conn.close()

################################################

if __name__ == '__main__':

    print "Iniciando processamento dos comentarios"
    connRead = mysql.connector.connect(host='127.0.0.1',
                                       user='root',
                                       db='analise'
                                       )

    cursorRead = connRead.cursor()

    select = """SELECT id_comentario, comentario_traduzido
                FROM scores_selenium
                WHERE score is null"""

    cursorRead.execute(select)

    for idc, comment in cursorRead:
        try:
            score_value = getScoreFromRepustate(comment)
        except Exception, e:
            print 'Erro: ', e

        score = Score(idc, score_value)
        updateNewScore(score)
        time.sleep(0.3)

################################################
#data = json.loads("""{"status": "OK", "results": [{"score": 0.2295, "id": "8419135"}, {"score": -0.20655, "id": "8184564"}, {"score": 0.36252, "id": "7992830"}, {"score": -0.20655, "id": "8127261"}, {"score": -0.2272, "id": "8165067"}, {"score": 0.60194, "id": "8088969"}, {"score": 0.22376, "id": "7870375"}, {"score": -0.20655, "id": "8271739"}, {"score": 0.0, "id": "8378658"}, {"score": 0.0, "id": "7824938"}, {"score": -0.20655, "id": "7859823"}, {"score": 0.0, "id": "7898258"}, {"score": 0.38042, "id": "7810995"}, {"score": 0.21802, "id": "8404125"}, {"score": 0.0, "id": "8002873"}, {"score": -0.03442, "id": "7977935"}, {"score": -0.20655, "id": "7867026"}, {"score": -0.01721, "id": "8023343"}, {"score": 0.38042, "id": "8174926"}, {"score": 0.03934, "id": "8033349"}, {"score": 0.25819, "id": "8108936"}, {"score": 0.0, "id": "8243490"}, {"score": -0.00516, "id": "8340527"}, {"score": -0.2295, "id": "8313977"}, {"score": 0.61877, "id": "8187670"}, {"score": 0.0, "id": "8371156"}, {"score": 0.0, "id": "8381408"}, {"score": -0.00393, "id": "7871674"}, {"score": 0.0, "id": "7763771"}, {"score": -0.23606, "id": "7985702"}, {"score": 0.0, "id": "8264981"}, {"score": 0.47504, "id": "8104154"}]}""")
