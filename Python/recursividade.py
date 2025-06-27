import tkinter as tk
from tkinter import ttk

# Algoritmos recursivos
def fatorial(n):
    if n == 0:
        return 1
    return n * fatorial(n - 1)

def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

def soma_n(n):
    if n == 0:
        return 0
    return n + soma_n(n - 1)

def potencia(x, n):
    if n == 0:
        return 1
    return x * potencia(x, n - 1)

# Função para aplicar o algoritmo recursivo selecionado
def aplicar_algoritmo():
    entrada = entrada_lista.get()
    try:
        if algoritmo_var.get() in ["Fatorial", "Fibonacci", "Soma N"]:
            n = int(entrada)
            if algoritmo_var.get() == "Fatorial":
                resultado = fatorial(n)
            elif algoritmo_var.get() == "Fibonacci":
                resultado = fibonacci(n)
            elif algoritmo_var.get() == "Soma N":
                resultado = soma_n(n)
        elif algoritmo_var.get() == "Potência":
            base, expoente = map(int, entrada.split(","))
            resultado = potencia(base, expoente)

        resultado_var.set(f"Resultado: {resultado}")
    except:
        resultado_var.set("Erro: insira os dados corretamente")

# GUI com Tkinter
janela = tk.Tk()
janela.title("Recursividade em Python")
janela.geometry("400x250")

algoritmo_var = tk.StringVar(value="Fatorial")
resultado_var = tk.StringVar()

entrada_label = tk.Label(janela, text="Digite o valor (ou base,expoente para potência):")
entrada_label.pack()

entrada_lista = tk.Entry(janela)
entrada_lista.pack(fill="x", padx=10)

algoritmo_menu = ttk.Combobox(janela, textvariable=algoritmo_var)
algoritmo_menu['values'] = ["Fatorial", "Fibonacci", "Soma N", "Potência"]
algoritmo_menu.pack(pady=10)

botao = tk.Button(janela, text="Executar", command=aplicar_algoritmo)
botao.pack()

resultado_label = tk.Label(janela, textvariable=resultado_var, wraplength=350, justify="center")
resultado_label.pack(pady=10)

janela.mainloop()