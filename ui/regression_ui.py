"""UI pour la régression linéaire.
Lecture CSV (x,y), ajustement via sklearn, affichage nuage et droite de régression.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from core.regression import linear_regression_fit


class RegressionUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.df = None
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self)
        frm.pack(fill="both", expand=True, padx=10, pady=10)

        left = ttk.Frame(frm)
        left.pack(side="left", fill="y", padx=(0, 10))

        ttk.Button(left, text="Charger CSV (x,y)", command=self.load_csv).pack(pady=(0, 8))
        ttk.Button(left, text="Calculer régression", command=self.on_fit).pack(pady=(0, 8))
        ttk.Button(left, text="Effacer", command=self.clear).pack()

        right = ttk.Frame(frm)
        right.pack(side="left", fill="both", expand=True)

        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        self.result_box = tk.Text(right, height=5, state="disabled")
        self.result_box.pack(fill="x", pady=(6, 0))

    def load_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if not path:
            return
        try:
            self.df = pd.read_csv(path)
            if "x" not in self.df.columns or "y" not in self.df.columns:
                messagebox.showerror("Format", "Le CSV doit contenir des colonnes 'x' et 'y'.")
                self.df = None
                return
            messagebox.showinfo("Chargé", f"{len(self.df)} points chargés depuis {path}")
            self._plot_points()
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de charger le CSV: {e}")

    def on_fit(self):
        if self.df is None:
            messagebox.showwarning("Aucune donnée", "Chargez d'abord un fichier CSV.")
            return
        result = linear_regression_fit(self.df["x"].values.reshape(-1, 1), self.df["y"].values)
        coef = result["coef"]
        intercept = result["intercept"]
        score = result["r2"]
        self.result_box.config(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.insert("1.0", f"y = {coef[0]:.6f} * x + {intercept:.6f}\nR^2 = {score:.6f}")
        self.result_box.config(state="disabled")
        self._plot_fit(result)

    def _plot_points(self):
        self.ax.clear()
        self.ax.scatter(self.df["x"], self.df["y"], s=20)
        self.ax.set_title("Nuage de points")
        self.canvas.draw()

    def _plot_fit(self, result):
        self.ax.clear()
        x = self.df["x"].values
        y = self.df["y"].values
        self.ax.scatter(x, y, s=20, label="Données")
        xs = pd.Series(sorted(x))
        ys = result["predict"](xs.values.reshape(-1, 1))
        self.ax.plot(xs, ys, label="Régression", linewidth=2)
        self.ax.set_title("Régression linéaire")
        self.ax.legend()
        self.canvas.draw()

    def clear(self):
        self.df = None
        self.ax.clear()
        self.canvas.draw()
        self.result_box.config(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.config(state="disabled")
