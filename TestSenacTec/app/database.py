import sqlite3

def get_conexao():
    return sqlite3.connect('vendas.db')

con = sqlite3.connect('vendas.db')
cur = con.cursor()

# Tabelas (já criadas anteriormente)
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
        preco_unit REAL NOT NULL,
        imagem TEXT
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