import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Função para conectar ao banco
def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="escola"
    )

# Função para cadastrar aluno
def cadastrar_aluno():
    nome = entry_nome.get()
    email = entry_email.get()

    if nome == "" or email == "":
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return

    try:
        conn = conectar()
        cursor = conn.cursor()
        sql = "INSERT INTO alunos (nome, email) VALUES (%s, %s)"
        cursor.execute(sql, (nome, email))
        conn.commit()
        messagebox.showinfo("Sucesso", "Aluno cadastrado com sucesso!")
        entry_nome.delete(0, tk.END)
        entry_email.delete(0, tk.END)
    except Exception as e:
        messagebox.showerror("Erro", str(e))
    finally:
        cursor.close()
        conn.close()

# Função para exibir alunos
def exibir_alunos():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM alunos")
        resultado = cursor.fetchall()

        texto_resultado.delete(1.0, tk.END)  # limpa o campo antes
        for aluno in resultado:
            texto_resultado.insert(tk.END, f"ID: {aluno[0]} - Nome: {aluno[1]} - Email: {aluno[2]}\n")
    except Exception as e:
        messagebox.showerror("Erro", str(e))
    finally:
        cursor.close()
        conn.close()

# Interface
janela = tk.Tk()
janela.title("Cadastro de Alunos")
janela.geometry("400x400")

# Campos
tk.Label(janela, text="Nome").pack()
entry_nome = tk.Entry(janela, width=40)
entry_nome.pack()

tk.Label(janela, text="Email").pack()
entry_email = tk.Entry(janela, width=40)
entry_email.pack()

# Botões
tk.Button(janela, text="Cadastrar", command=cadastrar_aluno).pack(pady=10)
tk.Button(janela, text="Exibir Alunos", command=exibir_alunos).pack(pady=5)

# Área de exibição
texto_resultado = tk.Text(janela, height=10, width=50)
texto_resultado.pack(pady=10)

janela.mainloop()
