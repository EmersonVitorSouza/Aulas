import tkinter as tk
from tkinter import ttk, scrolledtext
from tkinter import messagebox
import random # Importar o módulo random

# --- 1. Definindo os Jogadores e suas Habilidades (AGORA COM INTERVALOS DE PROBABILIDADE) ---
# Cada jogador terá um intervalo (min_prob, max_prob) para a probabilidade de arremesso.
JOGADORES = {
    "Armador": {"prob_arremesso_range": (0.6, 0.8)}, # Flutua entre 60% e 80%
    "Ala": {"prob_arremesso_range": (0.5, 0.7)},
    "Pivô": {"prob_arremesso_range": (0.4, 0.6)},
    "Arremessador": {"prob_arremesso_range": (0.7, 0.9)}, # Maior range para bons arremessadores
    "Defensor": {"prob_arremesso_range": (0.3, 0.5)}
}

# --- 2. A Função Recursiva de Análise da Jogada (Com probabilidade aleatória no arremesso) ---
def analisar_jogada(jogador_atual: str, jogadores_disponiveis: list, jogada_atual: list, profundidade_maxima: int) -> dict:
    """
    Analisa recursivamente as possíveis sequências de jogadas (passes e arremessos).

    Args:
        jogador_atual (str): O nome do jogador que está com a bola no momento.
        jogadores_disponiveis (list): Lista de jogadores que ainda podem receber um passe.
        jogada_atual (list): A sequência de ações (passes) até o momento.
        profundidade_maxima (int): Limite de passes para evitar recursão infinita.

    Returns:
        dict: Um dicionário com a melhor jogada encontrada (sequência de ações)
              e sua probabilidade de pontuação.
    """
    melhor_jogada_encontrada = {"sequencia": [], "probabilidade": -1.0}

    # --- Caso Base 1: O Jogador Atual Arremessa ---
    # Geramos uma probabilidade de arremesso aleatória dentro do range do jogador
    min_prob, max_prob = JOGADORES[jogador_atual]["prob_arremesso_range"]
    prob_acerto = random.uniform(min_prob, max_prob) # Gera um float aleatório no intervalo
    
    if prob_acerto > melhor_jogada_encontrada["probabilidade"]:
        melhor_jogada_encontrada = {
            "sequencia": jogada_atual + [f"Arremesso de {jogador_atual} (Prob Aleatória: {prob_acerto:.2f})"],
            "probabilidade": prob_acerto
        }

    # --- Caso Base 2: Atingiu a Profundidade Máxima de Passes ---
    if len(jogada_atual) >= profundidade_maxima:
        return melhor_jogada_encontrada

    # --- Caso Recursivo: O Jogador Atual Passa a Bola ---
    jogadores_para_passe = [j for j in jogadores_disponiveis if j != jogador_atual]

    for proximo_jogador in jogadores_para_passe:
        # Previne passar para o mesmo jogador que acabou de passar a bola (opcional, para jogadas mais realistas)
        if jogada_atual and proximo_jogador == jogada_atual[-1].split(" para ")[-1]:
            continue # Ignora passar de volta para quem acabou de te passar a bola

        nova_jogada = jogada_atual + [f"Passe de {jogador_atual} para {proximo_jogador}"]
        novos_jogadores_disponiveis = [j for j in jogadores_disponiveis if j != proximo_jogador]

        # Chamada recursiva para analisar a jogada a partir do próximo jogador
        resultado_sub_jogada = analisar_jogada(
            proximo_jogador,
            novos_jogadores_disponiveis,
            nova_jogada,
            profundidade_maxima
        )

        # Atualiza a melhor jogada encontrada se esta sub-jogada for melhor
        if resultado_sub_jogada["probabilidade"] > melhor_jogada_encontrada["probabilidade"]:
            melhor_jogada_encontrada = resultado_sub_jogada

    return melhor_jogada_encontrada

# --- 3. Construindo a Interface Tkinter (Mantida como estava) ---

class AnalisadorJogadasApp:
    def __init__(self, master):
        self.master = master
        master.title("Analisador de Jogadas de Basquete")
        master.geometry("600x400")

        master.configure(bg="#e0e0e0")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#e0e0e0")
        style.configure("TLabel", background="#e0e0e0", font=("Arial", 10))
        style.configure("TButton", font=("Arial", 10, "bold"), padding=6)
        style.configure("TCombobox", font=("Arial", 10))

        control_frame = ttk.Frame(master, padding="10")
        control_frame.pack(pady=10)

        ttk.Label(control_frame, text="Jogador com a Bola:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.jogador_inicial_var = tk.StringVar()
        self.jogador_inicial_combobox = ttk.Combobox(
            control_frame,
            textvariable=self.jogador_inicial_var,
            values=list(JOGADORES.keys()),
            state="readonly"
        )
        self.jogador_inicial_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.jogador_inicial_combobox.set("Armador")

        ttk.Label(control_frame, text="Profundidade Máxima de Passes:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.profundidade_var = tk.IntVar(value=3)
        self.profundidade_spinbox = ttk.Spinbox(
            control_frame,
            from_=1, to=5,
            textvariable=self.profundidade_var,
            width=5
        )
        self.profundidade_spinbox.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.analisar_button = ttk.Button(control_frame, text="Analisar Jogada", command=self.executar_analise)
        self.analisar_button.grid(row=2, column=0, columnspan=2, pady=10)

        result_frame = ttk.Frame(master, padding="10")
        result_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(result_frame, text="Melhor Sequência de Jogada:").pack(pady=(0, 5), anchor="w")
        self.sequencia_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD, width=60, height=8, font=("Arial", 9))
        self.sequencia_text.pack(fill=tk.BOTH, expand=True)
        self.sequencia_text.insert(tk.END, "Clique em 'Analisar Jogada' para ver o resultado.")
        self.sequencia_text.config(state=tk.DISABLED)

        self.probabilidade_label = ttk.Label(result_frame, text="Probabilidade de Pontuação: ")
        self.probabilidade_label.pack(pady=(10, 0), anchor="w")

    def executar_analise(self):
        jogador_inicial = self.jogador_inicial_var.get()
        profundidade_maxima = self.profundidade_var.get()

        if not jogador_inicial:
            messagebox.showwarning("Atenção", "Selecione o jogador inicial.")
            return

        jogadores_disponiveis = list(JOGADORES.keys())

        self.sequencia_text.config(state=tk.NORMAL)
        self.sequencia_text.delete(1.0, tk.END)
        
        try:
            resultado = analisar_jogada(
                jogador_inicial,
                jogadores_disponiveis,
                [],
                profundidade_maxima
            )

            for acao in resultado["sequencia"]:
                self.sequencia_text.insert(tk.END, acao + "\n")
            
            self.probabilidade_label.config(
                text=f"Probabilidade de Pontuação: {resultado['probabilidade']:.2%}"
            )
        except Exception as e:
            messagebox.showerror("Erro na Análise", f"Ocorreu um erro: {e}")
        finally:
            self.sequencia_text.config(state=tk.DISABLED)

# --- 4. Inicializa e executa a aplicação Tkinter ---
if __name__ == "__main__":
    root = tk.Tk()
    app = AnalisadorJogadasApp(root)
    root.mainloop()