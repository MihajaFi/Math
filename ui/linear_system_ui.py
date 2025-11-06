"""Interface pour résolution de systèmes linéaires (Ax = b).
Permet saisie manuelle ou chargement CSV simplifié.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from core.linear_system import solve_linear_system


class LinearSystemUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self)
        frm.pack(fill="both", expand=True, padx=10, pady=10)

        left = ttk.Frame(frm)
        left.pack(side="left", fill="y", padx=(0, 10))

        ttk.Label(left, text="Matrice A (ligne par ligne, virgule séparateur):").pack(anchor="w")
        self.text_a = tk.Text(left, width=40, height=10)
        self.text_a.pack()

        ttk.Label(left, text="Vecteur b (virgule séparateur):").pack(anchor="w", pady=(8, 0))
        self.entry_b = tk.Entry(left, width=40)
        self.entry_b.pack()

        btn_frame = ttk.Frame(left)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text="Charger CSV (A et b)", command=self.load_csv).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Résoudre", command=self.on_solve).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Effacer", command=self.clear).pack(side="left", padx=5)

        right = ttk.Frame(frm)
        right.pack(side="left", fill="both", expand=True)

        ttk.Label(right, text="Résultat:").pack(anchor="w")
        self.result_box = tk.Text(right, width=50, height=6, state="disabled")
        self.result_box.pack(fill="x", pady=(0, 10))

        # Graphique (pour systèmes 2x2)
        self.fig, self.ax = plt.subplots(figsize=(5, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv"), ("All", "*.*")])
        if not path:
            return
        try:
            data = np.loadtxt(path, delimiter=",")
            # suppose last column = b, rest = A
            A = data[:, :-1]
            b = data[:, -1]
            # fill UI
            self.text_a.delete("1.0", "end")
            a_lines = "\n".join(",".join(map(str, row)) for row in A)
            self.text_a.insert("1.0", a_lines)
            self.entry_b.delete(0, "end")
            self.entry_b.insert(0, ",".join(map(str, b)))
            messagebox.showinfo("Chargé", f"Fichier chargé: {path}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le fichier: {e}")

    def on_solve(self):
        try:
            A_text = self.text_a.get("1.0", "end").strip()
            if not A_text:
                messagebox.showwarning("Entrée", "Veuillez saisir la matrice A.")
                return
            A = np.array([[float(x) for x in row.split(",")] for row in A_text.splitlines()])
            b = np.array([float(x) for x in self.entry_b.get().split(",")])
            x = solve_linear_system(A, b)
            self._show_result(x)
            self._plot_if_2d(A, b, x)
        except Exception as e:
            messagebox.showerror("Erreur", f"Calcul impossible: {e}")

    def _show_result(self, x):
        self.result_box.config(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.insert("1.0", f"x = {np.array2string(x, precision=6)}")
        self.result_box.config(state="disabled")

    def _plot_if_2d(self, A, b, x):
        self.ax.clear()
        if A.shape == (2, 2):
            # plot the two lines A[0]·[x,y]=b0 and A[1]·[x,y]=b1
            xs = np.linspace(-10, 10, 400)
            # avoid vertical lines special case
            for i in range(2):
                a1, a2 = A[i]
                if abs(a2) > 1e-9:
                    ys = (b[i] - a1 * xs) / a2
                    self.ax.plot(xs, ys, label=f"Eq{i+1}")
                else:
                    xval = b[i] / a1
                    self.ax.axvline(xval, label=f"Eq{i+1}")
            self.ax.scatter([x[0]], [x[1]], color="black", label="Solution")
            self.ax.legend()
            self.ax.set_xlabel("x")
            self.ax.set_ylabel("y")
            self.ax.set_title("Visualisation 2D du système")
            self.canvas.draw()
        else:
            self.ax.text(0.5, 0.5, "Visualisation 2D disponible pour matrices 2x2 seulement",
                         ha="center", va="center")
            self.canvas.draw()

    def clear(self):
        self.text_a.delete("1.0", "end")
        self.entry_b.delete(0, "end")
        self.result_box.config(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.config(state="disabled")
        self.ax.clear()
        self.canvas.draw()
