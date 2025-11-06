"""UI principale — main_window.py
Crée les onglets et charge les modules (systèmes linéaires, régression, PL, stochastique).
"""
import tkinter as tk
from tkinter import ttk

from ui.linear_system_ui import LinearSystemUI
from ui.regression_ui import RegressionUI
from ui.linear_programming_ui import LinearProgrammingUI
from ui.stochastic_ui import StochasticUI


class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)

        # Onglet 1: système linéaire
        ls_frame = LinearSystemUI(notebook)
        notebook.add(ls_frame, text="Système linéaire")

        # Onglet 2: programmation linéaire
        lp_frame = LinearProgrammingUI(notebook)
        notebook.add(lp_frame, text="Programmation linéaire")

        # Onglet 3: régression
        rg_frame = RegressionUI(notebook)
        notebook.add(rg_frame, text="Régression linéaire")

        # Onglet 4: stochastique
        st_frame = StochasticUI(notebook)
        notebook.add(st_frame, text="Processus stochastiques")

        # Footer
        footer = ttk.Label(self, text="MathSolverApp — By Student | Modules: Linear system, LP, Regression, Markov",
                            anchor="center")
        footer.pack(side="bottom", fill="x")
