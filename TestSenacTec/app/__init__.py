from flask import Flask

app = Flask(__name__)
app.secret_key = 'chave-secreta-segura'  # para sessões

from app import routes
