import numpy as np
def gauss_elimination(A, b):
    """
    Implementación del método de eliminación de Gauss para resolver Ax = b
    """
    n = len(b)
    Ab = np.hstack((A, b.reshape(-1, 1)))

    for i in range(n):
        max_row = np.argmax(np.abs(Ab[i:, i])) + i
        Ab[[i, max_row]] = Ab[[max_row, i]]

        for j in range(i + 1, n):
            factor = Ab[j, i] / Ab[i, i]
            Ab[j] -= factor * Ab[i]

    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (Ab[i, -1] - np.dot(Ab[i, i + 1:n], x[i + 1:])) / Ab[i, i]

    return x