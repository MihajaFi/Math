"""core/linear_system.py
Fonctions pour résoudre des systèmes linéaires.
"""
import numpy as np


def solve_linear_system(A, b, method="numpy"):
    """
    Résout Ax = b.
    - A: tableau numpy (n,n)
    - b: vecteur numpy (n,) ou (n,1)
    - method: 'numpy' (par défaut) ou 'gauss' (implémentation simple)
    Retourne x (vecteur).
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float).reshape(-1)
    n, m = A.shape
    if n != m:
        raise ValueError("La matrice A doit être carrée.")
    if b.shape[0] != n:
        raise ValueError("Taille de b incompatible avec A.")

    if method == "numpy":
        # utilise la fonction robuste de numpy
        return np.linalg.solve(A, b)
    elif method == "gauss":
        # Implémentation basique d'élimination de Gauss (sans pivot complet)
        # Copie pour ne pas modifier A,b
        M = np.hstack((A.astype(float), b.reshape(-1, 1).astype(float)))
        n = M.shape[0]
        for k in range(n):
            # pivot simple
            if abs(M[k, k]) < 1e-12:
                # recherche d'un pivot
                for i in range(k + 1, n):
                    if abs(M[i, k]) > 1e-12:
                        M[[k, i]] = M[[i, k]]
                        break
            pivot = M[k, k]
            if abs(pivot) < 1e-12:
                raise np.linalg.LinAlgError("Pivot nul rencontré — matrice singulière ou mal posée.")
            M[k] = M[k] / pivot
            for i in range(n):
                if i != k:
                    M[i] = M[i] - M[k] * M[i, k]
        x = M[:, -1]
        return x
    else:
        raise ValueError("Méthode inconnue. Utiliser 'numpy' ou 'gauss'.")
