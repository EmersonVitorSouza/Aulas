# Importa as bibliotecas necessárias
from flask import Flask, render_template, request, redirect, jsonify  # Flask para criar rotas e páginas; request para pegar dados do formulário; jsonify para retornar JSON
import mysql.connector as banquinho# Biblioteca para conectar com o MySQL

# Cria a aplicação Flask
app = Flask(__name__)  # Instancia a aplicação Flask

# Função para conectar ao banco de dados MySQL
def conectar():
    return banquinho.connect(
        host="localhost",      # Endereço do servidor MySQL (localhost quando usando XAMPP)
        user="root",           # Usuário padrão do MySQL no XAMPP
        password="",           # Senha vazia por padrão no XAMPP
        database="escola"      # Nome do banco de dados a ser usado
    )

# Rota principal: exibe a página inicial com a lista de alunos
@app.route("/")
def index():
    try:
        conn = conectar()  # Conecta ao banco de dados
        cursor = conn.cursor()  # Cria o cursor para executar comandos SQL
        cursor.execute("SELECT * FROM alunos")  # Busca todos os registros da tabela alunos
        resultado = cursor.fetchall()  # Recupera todos os resultados da consulta
        alunos = [{"id": a[0], "nome": a[1], "email": a[2]} for a in resultado]  # Converte os resultados em uma lista de dicionários
        return render_template("index.html", alunos=alunos)  # Renderiza a página HTML com a lista de alunos
    except Exception as e:
        return f"Erro: {str(e)}", 500  # Retorna erro 500 com a mensagem se algo der errado
    finally:
        cursor.close()  # Fecha o cursor
        conn.close()    # Fecha a conexão com o banco

# Rota para cadastrar um novo aluno via formulário
@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form["nome"]  # Pega o nome do formulário
    email = request.form["email"]  # Pega o email do formulário
    senha = request.form["senha"]

    if nome == "" or email == "":
        return "Preencha todos os campos";

    try:
        conn = conectar()  # Conecta ao banco
        cursor = conn.cursor()  # Cria cursor
        sql = "INSERT INTO alunos (nome, email, senha) VALUES (%s, %s, %s)"  # SQL para inserir dados
        cursor.execute(sql, (nome, email, senha))  # Executa inserção
        conn.commit()  # Confirma as alterações no banco
        return "Aluno cadastrado com sucesso!"  # Retorna mensagem de sucesso
    except Exception as e:
        return f"Erro: {str(e)}", 500  # Retorna erro 500 com a mensagem de erro
    finally:
        cursor.close()  # Fecha o cursor
        conn.close()    # Fecha a conexão

# Rota que retorna os alunos em formato JSON (útil para JavaScript)
@app.route("/exibir", methods=["GET"])
def exibir():
    try:
        conn = conectar()  # Conecta ao banco
        cursor = conn.cursor()  # Cria cursor
        cursor.execute("SELECT * FROM alunos")  # Consulta todos os alunos
        resultado = cursor.fetchall()  # Recupera todos os registros
        alunos = [{"id": a[0], "nome": a[1], "email": a[2]} for a in resultado]  # Converte para lista de dicionários
        return jsonify(alunos)  # Retorna os dados como JSON
    except Exception as e:
        return f"Erro: {str(e)}", 500  # Retorna erro se algo der errado
    finally:
        cursor.close()  # Fecha o cursor
        conn.close()    # Fecha a conexão

# Ponto de entrada do programa
if __name__ == "__main__":
    app.run(debug=True)  # Inicia o servidor Flask em modo debug    