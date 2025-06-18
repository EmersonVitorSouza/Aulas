from controller.user_controller import UserController  # Importa o controller principal

if __name__ == "__main__":
    app = UserController()  # Cria a aplicação
    app.run()               # Inicia a interface gráfica
