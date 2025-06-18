class CadastrarModel:
    """Modelo para o cadastro de usuários.
    Esta classe representa um usuário e contém métodos para salvar os dados.
    """
    def __init__(self, nome, email, senha):
        self.nome = nome
        self.email = email
        self.senha = senha

    def salvar(self):
        # Aqui você pode implementar a lógica para salvar o usuário no banco de dados
        # Exemplo fictício:
        print(f"Usuário {self.nome} cadastrado com sucesso!")