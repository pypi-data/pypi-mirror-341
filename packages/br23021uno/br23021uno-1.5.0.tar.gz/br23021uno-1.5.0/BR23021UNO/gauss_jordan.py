import numpy as np

def gauss_jordan(coefficients, ind_terms):
    """
    Resuelve un sistema de ecuaciones lineales Ax = b usando el método de Gauss-Jordan.
    """
    coefficients = np.array(coefficients, dtype=float)
    ind_terms = np.array(ind_terms, dtype=float)

    n = len(ind_terms)
    equations = np.hstack([coefficients, ind_terms.reshape(-1, 1)])

    for i in range(n):
        max_row = max(range(i, n), key=lambda r: abs(equations[r, i]))
        equations[[i, max_row]] = equations[[max_row, i]]

        if np.isclose(equations[i, i], 0): 
            return None

        equations[i] /= equations[i, i]

        for j in range(n):
            if i != j:
                factor = equations[j, i]
                equations[j] -= factor * equations[i]

    return equations[:, -1]


