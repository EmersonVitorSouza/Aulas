import tkinter as tk

def somar():
    try:
        n1 = float(entrada1.get())
        n2 = float(entrada2.get())
        resultado.set(f"Resultado: {n1 + n2}")
    except ValueError:
        resultado.set("Digite números válidos!")

# Janela principal
window = tk.Tk()
window.title("Calculadora Simples")

# Entradas
tk.Label(window, text="Número 1").pack()
entrada1 = tk.Entry(window)
entrada1.pack()

tk.Label(window, text="Número 2").pack()
entrada2 = tk.Entry(window)
entrada2.pack()

# Botão de soma
tk.Button(window, text="Somar", command=somar).pack(pady=5)

# Resultado
resultado = tk.StringVar()
tk.Label(window, textvariable=resultado, font=("Arial", 14)).pack(pady=10)

# Iniciar a janela
window.mainloop()
