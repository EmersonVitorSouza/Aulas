import sqlite3  # Importa o módulo do SQLite, embutido no Python

# Classe que representa um usuário com nome e email
class User:
    def __init__(self, name, email):
        self.name = name      # Atributo nome
        self.email = email    # Atributo email

# Classe do modelo que manipula dados usando SQLite
class UserModel:
    def __init__(self, db_name="users.db"):
        self.conn = sqlite3.connect(db_name)  # Conecta (ou cria) um banco SQLite
        self.create_table()  # Cria a tabela se ela ainda não existir

    def create_table(self):
        cursor = self.conn.cursor()  # Cria um cursor para executar comandos SQL
        # Cria a tabela "users" com colunas id, name e email
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        ''')
        self.conn.commit()  # Salva (commita) a transação no banco

    def add_user(self, user):
        cursor = self.conn.cursor()  # Cria o cursor
        # Insere um novo usuário na tabela
        cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)', (user.name, user.email))
        self.conn.commit()  # Salva a inserção no banco

    def get_all_users(self):
        cursor = self.conn.cursor()  # Cria o cursor
        # Busca todos os usuários cadastrados
        cursor.execute('SELECT name, email FROM users')
        rows = cursor.fetchall()  # Recebe os resultados como lista de tuplas
        # Converte cada tupla (nome, email) para objeto User
        return [User(name, email) for name, email in rows]

    def __del__(self):
        self.conn.close()  # Fecha a conexão com o banco ao destruir o objeto
