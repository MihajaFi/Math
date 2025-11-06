# MathSolverApp

**MathSolverApp — Application graphique de résolution et de modélisation mathématique**

## Description
Application pédagogique en Python (Tkinter) qui propose :
- Résolution de systèmes linéaires (Gauss / numpy)
- Programmation linéaire (PuLP)
- Régression linéaire (scikit-learn)
- Processus stochastiques (chaînes de Markov, marche aléatoire)

## Structure
```
MathSolverApp/
├── ui/
├── core/
├── data/
├── main.py
├── requirements.txt
├── README.md
├── AI_USAGE.txt
└── rapport_technique.md
```

## Installation & exécution
1. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate    # Windows
```
2. Installer les dépendances :
```bash
pip install -r requirements.txt
```
3. Lancer l'application :
```bash
python main.py
```

## Utilisation rapide
- **Système linéaire** : saisir matrice A (ligne par ligne, valeurs séparées par des virgules) et vecteur b.
- **Programmation linéaire** : entrer fonction objectif (ex: `3*x1 + 2*x2`) et contraintes (`x1 + x2 <= 4`), puis `Résoudre`.
- **Régression** : charger un CSV contenant les colonnes `x` et `y`, puis calculer la régression.
- **Stochastique** : saisir une matrice de transition (P) et un vecteur initial; simuler.

## Remarques
- Tkinter est généralement fourni avec Python.
- Le code est modulaire et commenté pour faciliter l'apprentissage.
