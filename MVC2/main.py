# main.py

import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from bancoDeDados import get_conexao


# Função para cadastrar produto
def cadastrar_produto():
    nome = entry_nome.get().strip()
    preco = entry_preco.get().strip()
    if nome == "" or preco == "":
        messagebox.showerror("Erro", "Preencha todos os campos")
        return
    try:
        preco = float(preco)
    except ValueError:
        messagebox.showerror("Erro", "Preço inválido")
        return

    conn = get_conexao()
    cur = conn.cursor()
    cur.execute("INSERT INTO produtos (nome, preco_unit) VALUES (?, ?)", (nome, preco))
    conn.commit()
    conn.close()
    entry_nome.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    listar_produtos()
    messagebox.showinfo("Sucesso", "Produto cadastrado!")

# Função para registrar venda
def registrar_venda():
    try:
        item = tree_produtos.selection()[0]
        nome, preco = tree_produtos.item(item, "values")
        quantidade = int(entry_qtd.get())
        total = float(preco) * quantidade
        data = datetime.now().strftime('%Y-%m-%d')

        conn = get_conexao()
        cur = conn.cursor()
        cur.execute("SELECT id FROM produtos WHERE nome = ?", (nome,))
        produto_id = cur.fetchone()[0]
        cur.execute("INSERT INTO vendas (produto_id, data, quantidade, total) VALUES (?, ?, ?, ?)",
                    (produto_id, data, quantidade, total))
        conn.commit()
        conn.close()

        entry_qtd.delete(0, tk.END)
        listar_vendas()
        messagebox.showinfo("Sucesso", "Venda registrada!")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Função para listar produtos
def listar_produtos():
    for item in tree_produtos.get_children():
        tree_produtos.delete(item)
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute("SELECT nome, preco_unit FROM produtos")
    for nome, preco in cur.fetchall():
        tree_produtos.insert("", tk.END, values=(nome, preco))
    conn.close()

# Função para listar vendas
def listar_vendas():
    for item in tree_vendas.get_children():
        tree_vendas.delete(item)
    conn = get_conexao()
    cur = conn.cursor()
    cur.execute('''
        SELECT p.nome, v.data, v.quantidade, v.total
        FROM vendas v
        JOIN produtos p ON p.id = v.produto_id
    ''')
    for nome, data, qtd, total in cur.fetchall():
        tree_vendas.insert("", tk.END, values=(nome, data, qtd, f"R$ {total:.2f}"))
    conn.close()

# Interface
root = tk.Tk()
root.title("Sistema de Vendas")

# Cadastro de produto
tk.Label(root, text="Produto:").grid(row=0, column=0)
entry_nome = tk.Entry(root)
entry_nome.grid(row=0, column=1)

tk.Label(root, text="Preço Unitário:").grid(row=1, column=0)
entry_preco = tk.Entry(root)
entry_preco.grid(row=1, column=1)

btn_cadastrar = tk.Button(root, text="Cadastrar Produto", command=cadastrar_produto)
btn_cadastrar.grid(row=2, column=0, columnspan=2, pady=5)

# Lista de produtos
tree_produtos = ttk.Treeview(root, columns=("Nome", "Preço"), show="headings")
tree_produtos.heading("Nome", text="Nome")
tree_produtos.heading("Preço", text="Preço Unitário")
tree_produtos.grid(row=3, column=0, columnspan=2, pady=10)

# Venda
tk.Label(root, text="Quantidade:").grid(row=4, column=0)
entry_qtd = tk.Entry(root)
entry_qtd.grid(row=4, column=1)

btn_vender = tk.Button(root, text="Registrar Venda", command=registrar_venda)
btn_vender.grid(row=5, column=0, columnspan=2, pady=5)

# Lista de vendas
tree_vendas = ttk.Treeview(root, columns=("Produto", "Data", "Quantidade", "Total"), show="headings")
for col in ("Produto", "Data", "Quantidade", "Total"):
    tree_vendas.heading(col, text=col)
tree_vendas.grid(row=6, column=0, columnspan=2, pady=10)

listar_produtos()
listar_vendas()

root.mainloop()
