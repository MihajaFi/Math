"""UI de Programmation Linéaire (pulp).
Permet entrer une fonction objectif simple et contraintes (2 variables recommandées pour visualisation).
"""
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np

from core.linear_programming import solve_lp


class LinearProgrammingUI(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.create_widgets()

    def create_widgets(self):
        frm = ttk.Frame(self)
        frm.pack(fill="both", expand=True, padx=10, pady=10)

        left = ttk.Frame(frm)
        left.pack(side="left", fill="y", padx=(0, 10))

        ttk.Label(left, text="Fonction objectif (ex: 3*x1 + 2*x2):").pack(anchor="w")
        self.obj_entry = tk.Entry(left, width=40)
        self.obj_entry.pack()

        ttk.Label(left, text="Contraintes (une par ligne, ex: x1 + x2 <= 4):").pack(anchor="w", pady=(8, 0))
        self.cons_text = tk.Text(left, width=40, height=10)
        self.cons_text.pack()

        btn_frame = ttk.Frame(left)
        btn_frame.pack(pady=8)
        ttk.Button(btn_frame, text="Résoudre (max)", command=lambda: self.on_solve("max")).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Résoudre (min)", command=lambda: self.on_solve("min")).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Effacer", command=self.clear).pack(side="left", padx=5)

        right = ttk.Frame(frm)
        right.pack(side="left", fill="both", expand=True)

        ttk.Label(right, text="Résultat:").pack(anchor="w")
        self.result_box = tk.Text(right, width=50, height=8, state="disabled")
        self.result_box.pack(fill="x", pady=(0, 10))

        self.fig, self.ax = plt.subplots(figsize=(6, 5))
        self.canvas = FigureCanvasTkAgg(self.fig, master=right)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def on_solve(self, sense):
        try:
            obj = self.obj_entry.get().strip()
            cons_text = self.cons_text.get("1.0", "end").strip().splitlines()
            solution = solve_lp(obj, cons_text, sense=sense)
            # display
            self.result_box.config(state="normal")
            self.result_box.delete("1.0", "end")
            for k, v in solution.items():
                self.result_box.insert("end", f"{k} = {v}\n")
            self.result_box.config(state="disabled")
            # plot if 2 vars
            self._plot_2d(solution.get("_feasible_region_points", None), solution.get("objective_value", None),
                          solution.get("variables", None))
        except Exception as e:
            messagebox.showerror("Erreur", f"Résolution impossible: {e}")

    def _plot_2d(self, region_points, obj_val, variables):
        self.ax.clear()
        if region_points is None:
            self.ax.text(0.5, 0.5, "Visualisation 2D: fournissez un problème à 2 variables pour voir la région.",
                         ha="center", va="center")
            self.canvas.draw()
            return

        pts = np.array(region_points)
        # polygon
        self.ax.fill(pts[:, 0], pts[:, 1], alpha=0.3, label="Région admissible")
        # scatter feasible points
        self.ax.scatter(pts[:, 0], pts[:, 1], s=10)
        # optimal point
        if variables:
            x_opt = variables.get("x1", None)
            y_opt = variables.get("x2", None)
            if x_opt is not None and y_opt is not None:
                self.ax.scatter([x_opt], [y_opt], color="red", label=f"Optimum (val={obj_val:.3f})")
        self.ax.set_xlabel("x1")
        self.ax.set_ylabel("x2")
        self.ax.set_title("Visualisation 2D — Région admissible")
        self.ax.legend()
        self.canvas.draw()

    def clear(self):
        self.obj_entry.delete(0, "end")
        self.cons_text.delete("1.0", "end")
        self.result_box.config(state="normal")
        self.result_box.delete("1.0", "end")
        self.result_box.config(state="disabled")
        self.ax.clear()
        self.canvas.draw()
