import tkinter as tk  # Módulo da interface gráfica padrão do Python
from tkinter import messagebox  # Para mostrar mensagens de alerta/sucesso

class LoginView:
    def __init__(self, controller):
        self.controller = controller  # Referência ao controller
        self.root = tk.Tk()  # Cria a janela principal
        self.root.title("Login")  # Define o título da janela

        # Cria e posiciona o rótulo e campo para usuário
        tk.Label(self.root, text="Usuário:").grid(row=0, column=0)
        self.entry_username = tk.Entry(self.root)
        self.entry_username.grid(row=0, column=1)

        # Cria e posiciona o rótulo e campo para senha
        tk.Label(self.root, text="Senha:").grid(row=1, column=0)
        self.entry_password = tk.Entry(self.root, show='*')
        self.entry_password.grid(row=1, column=1)

        # Botão "Entrar", chama o método login
        self.btn_login = tk.Button(self.root, text="Entrar", command=self.login)
        self.btn_login.grid(row=2, column=0, columnspan=2, pady=5)

    def start(self):
        self.root.mainloop()  # Inicia o loop principal da interface

    def login(self):
        username = self.entry_username.get()  # Pega o valor digitado no campo usuário
        password = self.entry_password.get()  # Pega o valor do campo senha

        if username and password:
            if self.controller.login(username, password):  # Verifica as credenciais
                messagebox.showinfo("Sucesso", "Login realizado com sucesso!")  # Mensagem de sucesso
                self.root.destroy()  # Fecha a janela de login
            else:
                messagebox.showerror("Erro", "Usuário ou senha inválidos!")  # Mensagem de erro
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")  # Mostra alerta