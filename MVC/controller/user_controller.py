# Importa o modelo (UserModel e a classe User)
from model.user_model import UserModel, User
from model.login_model import LoginModel  # Importa a classe de login
# Importa a interface gráfica
from view.user_view import UserView
from view.login_view import LoginView  # Importa a interface de login

# Classe que faz a ponte entre View e Model
class UserController:
    def __init__(self):
        self.model = UserModel()     # Cria a instância do modelo
        self.view = UserView(self)   # Cria a view e passa a si mesmo (controller)
        self.model = LoginModel("admin", "password")
        self.view_login = LoginView(self)

    def run(self):
        self.view.start()  # Inicia o loop da interface gráfica

    def add_user(self, name, email):
        user = User(name, email)       # Cria um novo usuário
        self.model.add_user(user)      # Adiciona o usuário via model

    def get_users(self):
        return self.model.get_all_users()  # Busca usuários via model
    
    def validate_login(self, username, password):
        return self.model.validate_credentials(username, password)
