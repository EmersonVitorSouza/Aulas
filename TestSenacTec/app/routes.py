from flask import render_template, request, redirect, url_for, send_file, current_app
from app import app
from app.database import get_conexao
from app.ml_model import prever_faturamento
#from app.previsao import treinar_rede_neural
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import matplotlib.pyplot as plt
import os
import openai
import requests



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/produtos')
def listar_produtos():
    conexao = get_conexao()
    cursor = conexao.cursor()
    cursor.execute("SELECT id, nome, preco_unit FROM produtos")
    produtos = cursor.fetchall()
    conexao.close()

    return render_template('produtos.html', produtos=produtos)

@app.route('/vendas')
def listar_vendas():
    con = get_conexao()
    cur = con.cursor()
    cur.execute("""
        SELECT v.id, p.nome, v.data, v.quantidade, v.total
        FROM vendas v
        JOIN produtos p ON v.produto_id = p.id
    """)
    vendas = cur.fetchall()
    con.close()
    return render_template('vendas.html', vendas=vendas)


# Adicionar produto
@app.route('/adicionar-produto', methods=['GET', 'POST'])
def adicionar_produto():
    if request.method == 'POST':
        nome = request.form['nome']
        preco = float(request.form['preco'])

        con = get_conexao()
        cur = con.cursor()
        cur.execute("INSERT INTO produtos (nome, preco_unit) VALUES (?, ?)", (nome, preco))
        con.commit()
        con.close()

        return redirect(url_for('listar_produtos'))
    return render_template('adicionar_produto.html')


# Adicionar venda
@app.route('/adicionar-venda', methods=['GET', 'POST'])
def adicionar_venda():
    con = get_conexao()
    cur = con.cursor()
    cur.execute("SELECT id, nome FROM produtos")
    produtos = cur.fetchall()

    if request.method == 'POST':
        produto_id = int(request.form['produto_id'])
        data = request.form['data']
        quantidade = int(request.form['quantidade'])

        # Buscar preço do produto
        cur.execute("SELECT preco_unit FROM produtos WHERE id = ?", (produto_id,))
        preco = cur.fetchone()[0]
        total = preco * quantidade

        cur.execute("""
            INSERT INTO vendas (produto_id, data, quantidade, total)
            VALUES (?, ?, ?, ?)
        """, (produto_id, data, quantidade, total))

        con.commit()
        con.close()

        return redirect(url_for('listar_produtos'))  # ou para uma lista de vendas
    con.close()
    return render_template('adicionar_venda.html', produtos=produtos)


@app.route('/dashboard')
def dashboard():
    con = get_conexao()
    cur = con.cursor()

    # Vendas por produto
    cur.execute('''
        SELECT p.nome, SUM(v.quantidade) AS total_vendido
        FROM vendas v
        JOIN produtos p ON v.produto_id = p.id
        GROUP BY p.nome
    ''')
    vendas_por_produto = cur.fetchall()


    # Faturamento por produto (quantidade * preço_unit)
    cur.execute("""
        SELECT p.nome, SUM(v.quantidade * p.preco_unit)
        FROM vendas v
        JOIN produtos p ON v.produto_id = p.id
        GROUP BY p.nome
    """)
    faturamento_por_produto = cur.fetchall()

    con.close()

    return render_template('dashboard.html', vendas_por_produto=vendas_por_produto, faturamento_por_produto=faturamento_por_produto)


@app.route('/previsao')
def previsao():
    resultado = prever_faturamento()
    return render_template('previsao.html', resultado=resultado)

#@app.route('/prever')
#def previsao():
#    resultado = treinar_rede_neural()
#    return render_template('prever.html', resultado=resultado)


@app.route('/relatorio_pdf')
def gerar_relatorio_pdf():
    # Conexão com banco
    conn = get_conexao()
    cursor = conn.cursor()

    # Buscar dados dos produtos
    cursor.execute("SELECT nome, preco_unit FROM produtos")
    produtos = cursor.fetchall()

    # Buscar dados das vendas
    cursor.execute("""
        SELECT p.nome, v.quantidade, v.total
        FROM vendas v
        JOIN produtos p ON v.produto_id = p.id
    """)
    vendas = cursor.fetchall()

    # Buscar dados para gráficos
    cursor.execute("""
        SELECT p.nome, SUM(v.quantidade)
        FROM vendas v
        JOIN produtos p ON v.produto_id = p.id
        GROUP BY p.nome
    """)
    vendas_por_produto = cursor.fetchall()

    cursor.execute("""
        SELECT p.nome, SUM(v.total)
        FROM vendas v
        JOIN produtos p ON v.produto_id = p.id
        GROUP BY p.nome
    """)
    faturamento_por_produto = cursor.fetchall()

    conn.close()

    # Caminhos
    caminho_static = os.path.join(current_app.root_path, 'static')
    caminho_pdf = os.path.join(caminho_static, 'relatorio_final.pdf')
    caminho_vendas = os.path.join(caminho_static, 'vendas_por_produto.png')
    caminho_faturamento = os.path.join(caminho_static, 'faturamento_por_produto.png')

    # Gerar gráfico de Vendas por Produto
    if vendas_por_produto:
        nomes, quantidades = zip(*vendas_por_produto)
        plt.figure(figsize=(10, 5))
        plt.bar(nomes, quantidades, color='skyblue')
        plt.title('Vendas por Produto')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(caminho_vendas)
        plt.close()

    # Gerar gráfico de Faturamento por Produto
    if faturamento_por_produto:
        nomes, totais = zip(*faturamento_por_produto)
        plt.figure(figsize=(10, 5))
        plt.bar(nomes, totais, color='orange')
        plt.title('Faturamento por Produto')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(caminho_faturamento)
        plt.close()

    # Criar PDF
    c = canvas.Canvas(caminho_pdf, pagesize=A4)
    largura, altura = A4
    y = altura - 50

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Relatório de Vendas e Produtos")
    y -= 30

    # Produtos
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Produtos Registrados:")
    y -= 20
    data_produtos = [['Nome', 'Preço (R$)']] + list(produtos)
    tabela = Table(data_produtos, colWidths=[250, 100])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    tabela.wrapOn(c, 50, y)
    tabela.drawOn(c, 50, y - len(data_produtos) * 20)
    y -= len(data_produtos) * 20 + 40

    # Vendas
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Itens Vendidos:")
    y -= 20
    data_vendas = [['Produto', 'Quantidade', 'Total (R$)']] + list(vendas)
    tabela2 = Table(data_vendas, colWidths=[200, 80, 100])
    tabela2.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    tabela2.wrapOn(c, 50, y)
    tabela2.drawOn(c, 50, y - len(data_vendas) * 20)
    y -= len(data_vendas) * 20 + 40

    # Gráficos
    if os.path.exists(caminho_vendas):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Gráfico: Vendas por Produto")
        y -= 20
        c.drawImage(caminho_vendas, 50, y - 200, width=500, height=200)
        y -= 220

    if os.path.exists(caminho_faturamento):
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Gráfico: Faturamento por Produto")
        y -= 20
        c.drawImage(caminho_faturamento, 50, y - 200, width=500, height=200)
        y -= 220

    c.save()

    return send_file(caminho_pdf, as_attachment=True)

openai.api_key = 'sua_chave_aqui'

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    resposta = None
    if request.method == 'POST':
        pergunta = request.form['pergunta']
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": pergunta}
                ]
            )
            resposta = response.choices[0].message.content
        except Exception as e:
            resposta = f"Erro ao acessar a API: {e}"

    return render_template('chat.html', resposta=resposta)


API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
HF_TOKEN = "SuaChaveHuggAqui"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

@app.route('/chatHug', methods=['GET', 'POST'])
def chatHug():
    resposta = None
    if request.method == 'POST':
        pergunta = request.form['pergunta']
        prompt = f"<s>[INST] {pergunta} [/INST]"

        payload = {
            "inputs": prompt,
            "options": {"wait_for_model": True}
        }

        try:
            response = requests.post(API_URL, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            # A resposta vem em "generated_text" dentro de uma lista
            resposta = result[0]['generated_text'].split('[/INST]')[-1].strip()
        except Exception as e:
            resposta = f"Erro ao acessar a API: {e}"

    return render_template('chatHug.html', resposta=resposta)


import requests  # Adicione esta importação no início do arquivo

# Substitua pela sua chave da API DeepSeek
DEEPSEEK_API_KEY = 'sk-42ef96889d6248449d0cc43b4fcd7eee'
DEEPSEEK_API_URL = 'https://api.deepseek.com/v1/chat/completions'  # Verifique o endpoint correto

@app.route('/chatDeep', methods=['GET', 'POST'])
def chatDeep():
    resposta = None
    if request.method == 'POST':
        pergunta = request.form['pergunta']
        try:
            headers = {
                'Authorization': f'Bearer {DEEPSEEK_API_KEY}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                "model": "deepseek-chat",  # Verifique o nome do modelo correto
                "messages": [
                    {"role": "user", "content": pergunta}
                ]
            }
            
            response = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload)
            response_data = response.json()
            
            # Ajuste esta linha conforme a estrutura da resposta da API DeepSeek
            resposta = response_data['choices'][0]['message']['content']
            
        except Exception as e:
            resposta = f"Erro ao acessar a API: {e}"

    return render_template('chatDeep.html', resposta=resposta)
