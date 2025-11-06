"""core/stochastic.py
Simulations de chaînes de Markov et marches aléatoires.
"""
import numpy as np


def simulate_markov_chain(P, init, steps):
    """
    Simule une chaîne de Markov en probabilités (discrete time).
    - P: matrice (n,n) de transition (les lignes sum à 1)
    - init: vecteur initial (n,) (probabilité ou indicatrice)
    - steps: nombre d'étapes à simuler
    Retourne: trajectoire T shape (steps+1, n) des distributions.
    """
    P = np.array(P, dtype=float)
    init = np.array(init, dtype=float).reshape(-1)
    if P.shape[0] != P.shape[1]:
        raise ValueError("P doit être carrée.")
    n = P.shape[0]
    if init.shape[0] != n:
        raise ValueError("init de longueur incompatible.")
    traj = np.zeros((steps + 1, n))
    traj[0] = init / (init.sum() if init.sum() != 0 else 1)
    current = traj[0].copy()
    for t in range(1, steps + 1):
        current = current.dot(P)
        traj[t] = current
    return traj


def random_walk_1d(n_steps):
    """
    Simple marche aléatoire 1D: pas ±1 equiprobable.
    Retourne positions list length n_steps+1 starting at 0.
    """
    steps = np.random.choice([-1, 1], size=n_steps)
    pos = np.concatenate(([0], np.cumsum(steps)))
    return pos
