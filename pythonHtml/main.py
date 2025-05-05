from flask import Flask, render_template, request, redirect, jsonify
import mysql.connector

app = Flask(__name__)

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="escola"
    )

@app.route("/")
def index():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alunos")
        resultado = cursor.fetchall()
        alunos = [{"id": a[0], "nome": a[1], "email": a[2]} for a in resultado]
        return render_template("index.html", alunos=alunos)
    except Exception as e:
        return f"Erro: {str(e)}", 500
    finally:
        cursor.close()
        conn.close()

@app.route("/cadastrar", methods=["POST"])
def cadastrar():
    nome = request.form["nome"]
    email = request.form["email"]

    if nome == "" or email == "":
        return "Preencha todos os campos!", 400

    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "INSERT INTO alunos (nome, email) VALUES (%s, %s)"
        cursor.execute(sql, (nome, email))
        conn.commit()
        return "Aluno cadastrado com sucesso!"
    except Exception as e:
        return f"Erro: {str(e)}", 500
    finally:
        cursor.close()
        conn.close()

@app.route("/exibir", methods=["GET"])
def exibir():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alunos")
        resultado = cursor.fetchall()
        alunos = [{"id": a[0], "nome": a[1], "email": a[2]} for a in resultado]
        return jsonify(alunos)
    except Exception as e:
        return f"Erro: {str(e)}", 500
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    app.run(debug=True)
