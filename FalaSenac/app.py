from flask import Flask, request, jsonify, render_template
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)

DATABASE = 'fala_senac.sqlite'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS respostas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            turma TEXT NOT NULL,
            sentimento TEXT NOT NULL,
            turno TEXT NOT NULL,
            data_envio TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def enviar():
    turma = request.form.get('turma')
    sentimento = request.form.get('sentimento')
    turno = request.form.get('turno')
    data_envio = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    if not turma or not sentimento:
        return jsonify({'success': False, 'msg': 'Dados inválidos'}), 400
    
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO respostas (turma, sentimento, turno, data_envio)
        VALUES (?, ?, ?, ?)
    ''', (turma, sentimento, turno, data_envio))
    conn.commit()
    conn.close()
    return jsonify({'success': True, 'msg': 'Obrigado pela suas palavras!'})


def get_dados_por_turma():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT turma, sentimento, turno, data_envio FROM respostas')
    rows = cursor.fetchall()
    conn.close()

    dados = {}
    for turma, sentimento, turno, data_envio in rows:
        if turma not in dados:
            dados[turma] = []
        dados[turma].append({
            'sentimento': sentimento,
            'turno': turno,
            'data_envio': data_envio
        })
    return dados

@app.route('/dashboard')
def dashboard():
    dados_por_turma = get_dados_por_turma()
    turmas = list(dados_por_turma.keys())
    return render_template('dashboard.html', turmas=turmas, dados_por_turma=dados_por_turma)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
