import tkinter as tk  # Módulo da interface gráfica padrão do Python
from tkinter import messagebox  # Para mostrar mensagens de alerta/sucesso

# Classe responsável pela interface com o usuário
class UserView:
    def __init__(self, controller):
        self.controller = controller       # Referência ao controller
        self.root = tk.Tk()                # Cria a janela principal
        self.root.title("Cadastro de Usuários")  # Define o título da janela

        # Cria e posiciona o rótulo e campo para nome
        tk.Label(self.root, text="Nome:").grid(row=0, column=0)
        self.entry_name = tk.Entry(self.root)
        self.entry_name.grid(row=0, column=1)

        # Cria e posiciona o rótulo e campo para email
        tk.Label(self.root, text="Email:").grid(row=1, column=0)
        self.entry_email = tk.Entry(self.root)
        self.entry_email.grid(row=1, column=1)

        # Botão "Adicionar", chama o método add_user
        self.btn_add = tk.Button(self.root, text="Adicionar", command=self.add_user)
        self.btn_add.grid(row=2, column=0, columnspan=2, pady=5)

        # Botão "Listar", chama o método list_users
        self.btn_list = tk.Button(self.root, text="Listar", command=self.list_users)
        self.btn_list.grid(row=3, column=0, columnspan=2)

        # Caixa de listagem para mostrar os usuários
        self.listbox = tk.Listbox(self.root, width=40)
        self.listbox.grid(row=4, column=0, columnspan=2, pady=10)

    def start(self):
        self.root.mainloop()  # Inicia o loop principal da interface

    def add_user(self):
        name = self.entry_name.get()   # Pega o valor digitado no campo nome
        email = self.entry_email.get() # Pega o valor do campo email

        if name and email:
            self.controller.add_user(name, email)  # Envia os dados para o controller
            messagebox.showinfo("Sucesso", "Usuário adicionado!")  # Mostra mensagem de sucesso
            self.entry_name.delete(0, tk.END)  # Limpa o campo nome
            self.entry_email.delete(0, tk.END)  # Limpa o campo email
        else:
            messagebox.showwarning("Atenção", "Preencha todos os campos!")  # Mostra alerta

    def list_users(self, users=None):
        self.listbox.delete(0, tk.END)  # Limpa a listbox antes de atualizar
        users = users or self.controller.get_users()  # Busca usuários do controller se necessário
        for user in users:
            # Adiciona nome e email na lista
            self.listbox.insert(tk.END, f"{user.name} - {user.email}")
