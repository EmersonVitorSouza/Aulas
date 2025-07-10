import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading

def ping_ip(ip):
    try:
        output = subprocess.run(["ping", "-n", "1", "-w", "300", ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if "Resposta de" in output.stdout or "bytes=" in output.stdout:
            return True
    except Exception as e:
        return False
    return False

def verificar_rede(ip_base, saida_text):
    saida_text.delete(1.0, tk.END)
    saida_text.insert(tk.END, f"Verificando IPs da rede {ip_base}1 até {ip_base}254...\n\n")
    
    for i in range(1, 255):
        ip = f"{ip_base}{i}"
        if ping_ip(ip):
            saida_text.insert(tk.END, f"[ONLINE] {ip}\n")
        else:
            saida_text.insert(tk.END, f"[OFFLINE] {ip}\n")
        saida_text.update()

def iniciar_verificacao(ip_entry, saida_text):
    ip_base = ip_entry.get()
    if not ip_base.endswith("."):
        ip_base += "."
    thread = threading.Thread(target=verificar_rede, args=(ip_base, saida_text))
    thread.start()

# Criando a interface gráfica
janela = tk.Tk()
janela.title("Verificador de Nós Ativos na Rede")
janela.geometry("500x500")

tk.Label(janela, text="Digite o IP base da rede (ex: 192.168.0):").pack(pady=10)
ip_entry = tk.Entry(janela, width=20)
ip_entry.pack()

btn_verificar = tk.Button(janela, text="Verificar", command=lambda: iniciar_verificacao(ip_entry, saida_text))
btn_verificar.pack(pady=10)

saida_text = scrolledtext.ScrolledText(janela, width=60, height=20)
saida_text.pack(padx=10, pady=10)

janela.mainloop()