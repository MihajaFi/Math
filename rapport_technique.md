# Rapport technique — MathSolverApp

## 1. Introduction et objectif
MathSolverApp est une application pédagogique en Python fournissant des outils de calcul scientifique et de visualisation : résolution de systèmes linéaires, programmation linéaire, régression linéaire et simulations stochastiques. L'objectif est d'offrir une interface simple pour expérimenter des méthodes mathématiques classiques et observer leurs résultats graphiquement.

## 2. Description des modules
- `Système linéaire` : saisie de A et b, résolution via `numpy.linalg.solve` ou implémentation Gauss simple.
- `Programmation linéaire` : résolution par PuLP, parser simple d'expressions linéaires et contraintes. Visualisation 2D pour problèmes à 2 variables.
- `Régression linéaire` : lecture CSV (colonnes `x`, `y`), fit via `sklearn.linear_model.LinearRegression`, affichage droite de régression et R².
- `Processus stochastiques` : simulation de chaînes de Markov (distribution au fil des étapes) et marche aléatoire 1D.

## 3. Algorithmes et méthodes
- **Gauss** : élimination de Gauss avec pivotation simple (implémentation pédagogique).
- **Solve (numpy)** : `numpy.linalg.solve` pour robustesse numérique.
- **Programmation linéaire** : modèle PuLP (`LpProblem`) avec variables à borne 0 et résolution par le solveur par défaut.
- **Régression** : moindres carrés via `LinearRegression` de scikit-learn, calcul du score R².
- **Markov** : multiplication répétée de la distribution initiale par la matrice de transition.

## 4. Captures d'écran
- L'application génère automatiquement des graphiques matplotlib intégrés à Tkinter.
- (Insérer ici des captures d'écran si souhaité. Ex : `screenshots/ls_2x2.png`, `screenshots/regression.png`.)

## 5. Jeux de tests réalisés
- `data/regression_sample.csv` : petit jeu de test pour la régression.
- Exemple système 2x2 :
  ```
  A = [[1, -1],
       [2, 1]]
  b = [0, 5]
  ```
- Exemple LP : `Maximize 3*x1 + 2*x2` sous `x1 + x2 <= 4`, `x1 >= 0`, `x2 >= 0`.

## 6. Limites et pistes d'amélioration
- Parser LP basique : ne gère pas toutes les formes (termes constants, variables non-standard, bornes négatives). Améliorer le parser ou exposer une UI d'édition structurée.
- Gauss : pivotation pourrait être améliorée (pivot partiel/total) pour stabilité.
- Solver LP : permettre choix de solveur (CBC, GLPK).
- Tests unitaires : ajouter `pytest` et jeux de tests automatisés.
- Export : offre d'export PDF/CSV des résultats et rapports.

## 7. Conclusion
Le prototype offre une base solide pour explorer plusieurs méthodes mathématiques. L'architecture sépare clairement UI et logique (core), facilitant tests et extensions. Pour un usage en contexte académique, intégrer tests, documenter contributions humaines (si nécessaire) et renforcer la robustesse numérique.
