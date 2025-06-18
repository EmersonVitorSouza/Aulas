from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
import os
import fitz  # PyMuPDF
import openai
import json

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Se quiser, defina sua chave aqui (para testes, com limite de segurança)
# openai.api_key = 'sua-chave-aqui'

def extrair_texto_pdf(caminho_pdf):
    texto = ""
    with fitz.open(caminho_pdf) as doc:
        for pagina in doc:
            texto += pagina.get_text()
    return texto

def gerar_datas_uteis(data_inicio, data_fim, horas_por_dia, carga_total):
    datas = []
    data = data_inicio
    horas_acumuladas = 0

    while data <= data_fim and horas_acumuladas < carga_total:
        if data.weekday() < 5:  # Segunda a sexta
            datas.append(data)
            horas_acumuladas += horas_por_dia
        data += timedelta(days=1)
    
    return datas

def simular_resposta_ia(conteudo_pdf, datas):
    # Simula uma resposta da IA (depois substituímos pela chamada real)
    temas = conteudo_pdf.strip().split("\n")
    temas = [t.strip() for t in temas if len(t.strip()) > 10][:len(datas)]  # limita ao núm
