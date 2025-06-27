import tkinter as tk
from tkinter import ttk

# Algoritmos de ordenação
def bubble_sort(lista):
    n = len(lista)
    for i in range(n):
        for j in range(0, n - i - 1):
            if lista[j] > lista[j + 1]:
                lista[j], lista[j + 1] = lista[j + 1], lista[j]
    return lista

def selection_sort(lista):
    for i in range(len(lista)):
        menor = i
        for j in range(i + 1, len(lista)):
            if lista[j] < lista[menor]:
                menor = j
        lista[i], lista[menor] = lista[menor], lista[i]
    return lista

def insertion_sort(lista):
    for i in range(1, len(lista)):
        chave = lista[i]
        j = i - 1
        while j >= 0 and chave < lista[j]:
            lista[j + 1] = lista[j]
            j -= 1
        lista[j + 1] = chave
    return lista

def gnome_sort(lista):
    i = 0
    while i < len(lista):
        if i == 0 or lista[i] >= lista[i - 1]:
            i += 1
        else:
            lista[i], lista[i - 1] = lista[i - 1], lista[i]
            i -= 1
    return lista

def quick_sort(lista):
    if len(lista) <= 1:
        return lista
    else:
        pivo = lista[0]
        menores = quick_sort([x for x in lista[1:] if x <= pivo])
        maiores = quick_sort([x for x in lista[1:] if x > pivo])
        return menores + [pivo] + maiores

def merge_sort(lista):
    if len(lista) > 1:
        meio = len(lista) // 2
        esquerda = merge_sort(lista[:meio])
        direita = merge_sort(lista[meio:])

        resultado = []
        i = j = 0
        while i < len(esquerda) and j < len(direita):
            if esquerda[i] < direita[j]:
                resultado.append(esquerda[i])
                i += 1
            else:
                resultado.append(direita[j])
                j += 1
        resultado += esquerda[i:]
        resultado += direita[j:]
        return resultado
    else:
        return lista

# Função para aplicar o algoritmo selecionado
def aplicar_ordenacao():
    entrada = entrada_lista.get()
    try:
        lista = list(map(int, entrada.split(",")))
    except:
        resultado_var.set("Erro: insira números separados por vírgula")
        return

    algoritmo = algoritmo_var.get()
    if algoritmo == "Bubble Sort":
        resultado = bubble_sort(lista)
    elif algoritmo == "Selection Sort":
        resultado = selection_sort(lista)
    elif algoritmo == "Insertion Sort":
        resultado = insertion_sort(lista)
    elif algoritmo == "Gnome Sort":
        resultado = gnome_sort(lista)
    elif algoritmo == "Quick Sort":
        resultado = quick_sort(lista)
    elif algoritmo == "Merge Sort":
        resultado = merge_sort(lista)

    resultado_var.set(f"Resultado: {resultado}")

# GUI com Tkinter
janela = tk.Tk()
janela.title("Algoritmos de Ordenação")
janela.geometry("400x250")

algoritmo_var = tk.StringVar(value="Bubble Sort")
resultado_var = tk.StringVar()

entrada_label = tk.Label(janela, text="Digite números separados por vírgula:")
entrada_label.pack()

entrada_lista = tk.Entry(janela)
entrada_lista.pack(fill="x", padx=10)

algoritmo_menu = ttk.Combobox(janela, textvariable=algoritmo_var)
algoritmo_menu['values'] = ["Bubble Sort", "Selection Sort", "Insertion Sort", "Gnome Sort", "Quick Sort", "Merge Sort"]
algoritmo_menu.pack(pady=10)

botao = tk.Button(janela, text="Ordenar", command=aplicar_ordenacao)
botao.pack()

resultado_label = tk.Label(janela, textvariable=resultado_var, wraplength=350, justify="center")
resultado_label.pack(pady=10)

janela.mainloop()
