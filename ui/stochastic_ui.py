"""UI pour processus stochastiques: Chaîne de Markov et marche aléatoire.
Simulations simples et visualisation.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

from core.stochastic import simulate_markov_chain, random_walk_1d


class StochasticUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self)
        frm.pack(fill="both", expand=True, padx=10, pady=10)

        left = ttk.Frame(frm)
        left.pack(side="left", fill="y", padx=(0, 10))

        # Markov
        ttk.Label(left, text="Matrice de transition P (ligne par ligne, virgule sep):").pack(anchor="w")
        self.p_text = tk.Text(left, width=40, height=8)
        self.p_text.pack()

        ttk.Label(left, text="Etat initial (vecteur):").pack(anchor="w", pady=(6, 0))
        self.p_init = tk.Entry(left, width=40)
        self.p_init.pack()

        ttk.Label(left, text="Nombre d'étapes:").pack(anchor="w", pady=(6, 0))
        self.steps_entry = tk.Entry(left, width=20)
        self.steps_entry.insert(0, "10")
        self.steps_entry.pack()

        ttk.Button(left, text="Simuler Markov", command=self.on_markov).pack(pady=(8, 4))
        ttk.Separator(left, orient="horizontal").pack(fill="x", pady=6)

        ttk.Label(left, text="Marche aléatoire 1D (n étapes):").pack(anchor="w")
        self.walk_steps = tk.Entry(left, width=20)
        self.walk_steps.insert(0, "100")
        self.walk_steps.pack()
        ttk.Button(left, text="Simuler marche 1D", command=self.on_walk).pack(pady=(6, 4))

        right = ttk.Frame(frm)
        right.pack(side="left", fill="both", expand=True)

        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def on_markov(self):
        try:
            P_text = self.p_text.get("1.0", "end").strip()
            P = np.array([[float(x) for x in row.split(",")] for row in P_text.splitlines()])
            init = np.array([float(x) for x in self.p_init.get().split(",")])
            steps = int(self.steps_entry.get())
            traj = simulate_markov_chain(P, init, steps)
            # plot
            self.ax.clear()
            for i in range(P.shape[0]):
                self.ax.plot(range(steps + 1), traj[:, i], label=f"State {i}")
            self.ax.set_xlabel("Étape")
            self.ax.set_ylabel("Probabilité")
            self.ax.set_title("Évolution des probabilités (Markov)")
            self.ax.legend()
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Erreur", f"Simulation Markov impossible: {e}")

    def on_walk(self):
        try:
            n = int(self.walk_steps.get())
            path = random_walk_1d(n)
            self.ax.clear()
            self.ax.plot(range(len(path)), path, marker="o")
            self.ax.set_xlabel("Étape")
            self.ax.set_ylabel("Position")
            self.ax.set_title("Marche aléatoire 1D")
            self.canvas.draw()
        except Exception as e:
            messagebox.showerror("Erreur", f"Simulation marche impossible: {e}")
