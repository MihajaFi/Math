"""main.py
Point d'entrée de l'application MathSolverApp.
Lance la fenêtre principale Tkinter définie dans ui/main_window.py
"""
import tkinter as tk
from ui.main_window import MainWindow


def main():
    root = tk.Tk()
    root.title("MathSolverApp — Résolution & Modélisation Mathématique")
    root.geometry("1000x700")
    app = MainWindow(master=root)
    app.pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()
