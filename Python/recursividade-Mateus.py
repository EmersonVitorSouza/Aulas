import tkinter as tk
from tkinter import messagebox

# Função recursiva para somar os placares
def calcular_agregado_recursivo(placares, total=0):
    if not placares:
        return total
    return calcular_agregado_recursivo(placares[1:], total + placares[0])

# Função para registrar o placar do jogo de ida
def registrar_ida():
    try:
        time_a = entry_time_a.get()
        time_b = entry_time_b.get()
        placar_a = int(entry_placar_a_ida.get())
        placar_b = int(entry_placar_b_ida.get())

        if not time_a or not time_b:
            messagebox.showwarning("Entrada Inválida", "Por favor, insira os nomes dos dois times.")
            return

        placares["ida"] = {
            "time_a": time_a,
            "time_b": time_b,
            "placar_a": placar_a,
            "placar_b": placar_b
        }

        messagebox.showinfo("Placar Registrado", "Placar do jogo de ida registrado com sucesso.")
    except ValueError:
        messagebox.showwarning("Entrada Inválida", "Por favor, insira placares válidos para os times.")

# Função para registrar o placar do jogo de volta e calcular o agregado
def registrar_volta():
    try:
        placar_a = int(entry_placar_a_volta.get())
        placar_b = int(entry_placar_b_volta.get())

        if "ida" not in placares:
            messagebox.showwarning("Jogo de Ida Não Registrado", "Registre primeiro o placar do jogo de ida.")
            return

        placares["volta"] = {
            "placar_a": placar_a,
            "placar_b": placar_b
        }

        time_a = placares["ida"]["time_a"]
        time_b = placares["ida"]["time_b"]

        total_a = calcular_agregado_recursivo([
            placares["ida"]["placar_a"], 
            placares["volta"]["placar_a"]
        ])
        total_b = calcular_agregado_recursivo([
            placares["ida"]["placar_b"], 
            placares["volta"]["placar_b"]
        ])

        resultado_texto.set(f"Agregado Final:\n{time_a}: {total_a} x {total_b} :{time_b}")
        messagebox.showinfo("Agregado Calculado", "Placar agregado calculado com sucesso.")
    except ValueError:
        messagebox.showwarning("Entrada Inválida", "Por favor, insira placares válidos para os times.")

# Configuração da interface Tkinter
root = tk.Tk()
root.title("Calculadora de Agregado - Futebol")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(pady=10)

placares = {}

# Entrada de dados do jogo de ida
label_ida = tk.Label(frame, text="Jogo de Ida")
label_ida.grid(row=0, column=0, columnspan=4, pady=5)

label_time_a = tk.Label(frame, text="Time A:")
label_time_a.grid(row=1, column=0, padx=5, pady=5)
entry_time_a = tk.Entry(frame)
entry_time_a.grid(row=1, column=1, padx=5, pady=5)

label_time_b = tk.Label(frame, text="Time B:")
label_time_b.grid(row=1, column=2, padx=5, pady=5)
entry_time_b = tk.Entry(frame)
entry_time_b.grid(row=1, column=3, padx=5, pady=5)

label_placar_a_ida = tk.Label(frame, text="Placar Time A:")
label_placar_a_ida.grid(row=2, column=0, padx=5, pady=5)
entry_placar_a_ida = tk.Entry(frame)
entry_placar_a_ida.grid(row=2, column=1, padx=5, pady=5)

label_placar_b_ida = tk.Label(frame, text="Placar Time B:")
label_placar_b_ida.grid(row=2, column=2, padx=5, pady=5)
entry_placar_b_ida = tk.Entry(frame)
entry_placar_b_ida.grid(row=2, column=3, padx=5, pady=5)

botao_registrar_ida = tk.Button(frame, text="Registrar Ida", command=registrar_ida)
botao_registrar_ida.grid(row=3, column=0, columnspan=4, pady=10)

# Entrada de dados do jogo de volta
label_volta = tk.Label(frame, text="Jogo de Volta")
label_volta.grid(row=4, column=0, columnspan=4, pady=5)

label_placar_a_volta = tk.Label(frame, text="Placar Time A:")
label_placar_a_volta.grid(row=5, column=0, padx=5, pady=5)
entry_placar_a_volta = tk.Entry(frame)
entry_placar_a_volta.grid(row=5, column=1, padx=5, pady=5)

label_placar_b_volta = tk.Label(frame, text="Placar Time B:")
label_placar_b_volta.grid(row=5, column=2, padx=5, pady=5)
entry_placar_b_volta = tk.Entry(frame)
entry_placar_b_volta.grid(row=5, column=3, padx=5, pady=5)

botao_registrar_volta = tk.Button(frame, text="Registrar Volta e Calcular", command=registrar_volta)
botao_registrar_volta.grid(row=6, column=0, columnspan=4, pady=10)

resultado_texto = tk.StringVar()
resultado_label = tk.Label(root, textvariable=resultado_texto, justify="left")
resultado_label.pack(pady=10)

root.mainloop()
