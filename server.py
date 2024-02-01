#env\Scripts\python.exe
# -*- coding: utf-8 -*-

import os
from flask import Flask, request, render_template, url_for, redirect, json
import sqlite3

app = Flask(__name__, static_folder='public', template_folder='views')

app.secret_key = os.environ.get('SECRET')
usuario = 'Ninguém'
mensagem = 'Nada'

def access_db(command: str, params, method: str):
    conn = sqlite3.connect('message.db')
    cursor = conn.cursor()
    cursor.execute(command, params)
    results = cursor.fetchall() if method=='f' else conn.commit()
    conn.close()
    return results

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        try:
            access_db('UPDATE mensagem SET usuario=(?), mensagem=(?)', (request.form["nome"], request.form["mensagem"],), 'c')
            return render_template('index.html', classe='sucesso', retorno='funcionou')
        except Exception as e:
            return render_template('index.html', classe='erro', retorno=e)
    
    return render_template('index.html') 

@app.route('/dados')
def dados():
    rawData = access_db('SELECT * FROM mensagem', (), 'f')
    data = {
        "user": rawData[0][0],
        "message": rawData[0][1]
    }
    return json.dumps(data)


if __name__ == '__main__':
    access_db('''
        CREATE TABLE IF NOT EXISTS mensagem (
            usuario TEXT,
            mensagem TEXT
        )
    ''', (), 'c')
    access_db('INSERT INTO mensagem(usuario, mensagem) SELECT ?, ? WHERE NOT EXISTS(SELECT 1 FROM mensagem)', ('Usuario','Mensagem teste!',), 'c')
    app.run(debug=True)