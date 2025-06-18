# banco.py

import sqlite3

def get_conexao():
    return sqlite3.connect('vendas.db')

con = get_conexao()
cur = con.cursor()

# Criar tabela de usuários
cur.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    )
''')

# Criar tabela de produtos
cur.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        preco_unit REAL NOT NULL
    )
''')

# Criar tabela de vendas
cur.execute('''
    CREATE TABLE IF NOT EXISTS vendas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        data DATE NOT NULL,
        quantidade INTEGER NOT NULL,
        total REAL NOT NULL,
        FOREIGN KEY (produto_id) REFERENCES produtos(id)
    )
''')

con.commit()
con.close()

print("Banco de dados e tabelas criados com sucesso.")
