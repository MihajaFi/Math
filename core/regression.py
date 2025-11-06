"""core/regression.py
Régression linéaire simple using sklearn LinearRegression (wrapper pédagogique).
"""
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import numpy as np


def linear_regression_fit(X, y):
    """
    Fit a linear regression.
    - X: array-like (n_samples, n_features)
    - y: array-like (n_samples,)
    Retourne dict: coef, intercept, r2, predict(function)
    """
    X = np.array(X)
    y = np.array(y)
    model = LinearRegression()
    model.fit(X, y)
    y_pred = model.predict(X)
    result = {
        "coef": model.coef_,
        "intercept": float(model.intercept_),
        "r2": r2_score(y, y_pred),
        "predict": lambda Xnew: model.predict(np.array(Xnew).reshape(-1, X.shape[1])),
        "model": model
    }
    return result
