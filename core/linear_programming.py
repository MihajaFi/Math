"""core/linear_programming.py
Résolution de problèmes linéaires simples à l'aide de PuLP.
Le parser ici est volontairement simple et pédagogique.
"""
from pulp import LpProblem, LpVariable, lpSum, LpMaximize, LpMinimize, LpStatus, value
import re
import numpy as np
from itertools import product


def _parse_linear_expr(expr):
    """
    Parse une expression linéaire simple comme '3*x1 + 2*x2 - x3'
    Retourne dict variable->coefficient.
    """
    expr = expr.replace(" ", "")
    # ajouter + devant si commence par variable
    expr = re.sub(r"(?<!^)(?=[+-])", " ", expr)
    tokens = expr.replace("*", "").split()
    coeffs = {}
    for token in tokens:
        if token == "":
            continue
        # token peut être "+3x1" ou "-x2" ou "x1"
        m = re.match(r"([+-]?)(\d*\.?\d*)?([a-zA-Z]\d*)", token)
        if not m:
            raise ValueError(f"Impossible de parser le terme: {token}")
        sign, num, var = m.groups()
        sign = -1.0 if sign == "-" else 1.0
        coef = float(num) if num not in (None, "") else 1.0
        coeffs[var] = coeffs.get(var, 0.0) + sign * coef
    return coeffs


def _parse_constraint(constr):
    """
    Parse contrainte de forme 'x1 + 2*x2 <= 5' en (lhs dict, op, rhs float)
    """
    if "<=" in constr:
        lhs, rhs = constr.split("<=")
        op = "<="
    elif ">=" in constr:
        lhs, rhs = constr.split(">=")
        op = ">="
    elif "=" in constr:
        lhs, rhs = constr.split("=")
        op = "="
    else:
        raise ValueError("Contrainte doit contenir <=, >= ou =")
    lhs_dict = _parse_linear_expr(lhs)
    rhs_val = float(rhs)
    return lhs_dict, op, rhs_val


def _collect_vars(obj_str, constraints):
    vars_set = set()
    # obj
    for var in re.findall(r"[a-zA-Z]\d*", obj_str):
        vars_set.add(var)
    for c in constraints:
        for var in re.findall(r"[a-zA-Z]\d*", c):
            vars_set.add(var)
    # sort for consistency
    return sorted(vars_set)


def solve_lp(objective_str, constraints_list, sense="max"):
    """
    Résout un problème LP simple.
    - objective_str: chaîne, ex "3*x1 + 2*x2"
    - constraints_list: list de chaînes
    - sense: "max" ou "min"
    Retourne dict contenant variables, objective_value, statut, et points de région si 2 variables.
    """
    vars_names = _collect_vars(objective_str, constraints_list)
    if not vars_names:
        raise ValueError("Aucune variable trouvée dans le problème.")
    prob = LpProblem("LP", LpMaximize if sense == "max" else LpMinimize)
    lp_vars = {v: LpVariable(v, lowBound=0) for v in vars_names}  # borne 0 par défaut

    # parser et ajouter fonction objectif
    obj_coeffs = _parse_linear_expr(objective_str)
    prob += lpSum([coef * lp_vars[var] for var, coef in obj_coeffs.items() if var in lp_vars])

    # contraintes
    for c in constraints_list:
        lhs_dict, op, rhs_val = _parse_constraint(c)
        lhs = lpSum([coeff * lp_vars[var] for var, coeff in lhs_dict.items() if var in lp_vars])
        if op == "<=":
            prob += lhs <= rhs_val
        elif op == ">=":
            prob += lhs >= rhs_val
        else:
            prob += lhs == rhs_val

    prob.solve()

    res = {"status": LpStatus[prob.status], "objective_value": value(prob.objective)}
    # variables
    res_vars = {}
    for v in vars_names:
        res_vars[v] = lp_vars[v].value()
    res["variables"] = res_vars

    # If 2 variables, compute feasible polygon by brute force sampling of intersection points
    if len(vars_names) == 2:
        # list all combination of constraint boundaries intersections
        # approximate by computing intersections of pairs of lines (ignoring inequalities directions) then filter feasible
        eqs = []
        for c in constraints_list:
            lhs_dict, op, rhs_val = _parse_constraint(c)
            # convert to coefficients vector
            a = np.array([lhs_dict.get(vars_names[0], 0.0), lhs_dict.get(vars_names[1], 0.0)])
            b = rhs_val
            eqs.append((a, b, op))
        pts = []
        # consider intersections of each pair of (a·x = b)
        for (a1, b1, _), (a2, b2, _) in product(eqs, eqs):
            A = np.vstack([a1, a2])
            try:
                pt = np.linalg.solve(A, np.array([b1, b2]))
                pts.append(tuple(pt))
            except Exception:
                continue
        # add axis intercepts (0 bound)
        pts.append((0.0, 0.0))
        # filter unique and feasible
        uniq = list({(round(p[0], 8), round(p[1], 8)): p for p in pts}.values())
        feasible = []
        for p in uniq:
            ok = True
            for a, b, op in eqs:
                lhs = a.dot(np.array(p))
                if op == "<=" and lhs > b + 1e-6:
                    ok = False
                if op == ">=" and lhs < b - 1e-6:
                    ok = False
                if op == "=" and abs(lhs - b) > 1e-6:
                    ok = False
            if ok and p[0] >= -1e-8 and p[1] >= -1e-8:  # lowBound=0
                feasible.append(p)
        # convex hull order
        if feasible:
            arr = np.array(feasible)
            # sort by angle around centroid
            c = arr.mean(axis=0)
            angles = np.arctan2(arr[:, 1] - c[1], arr[:, 0] - c[0])
            order = np.argsort(angles)
            hull = arr[order].tolist()
            res["_feasible_region_points"] = hull
        else:
            res["_feasible_region_points"] = None

    return res
