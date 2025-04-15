import numpy as np

def crammer(A, b):
    """
    Resuelve el sistema Ax = b utilizando la regla de Cramer.
    
    Parámetros:
    - A: np.array o lista de listas que representa la matriz de coeficientes (n x n).
    - b: np.array o lista que representa el vector de términos independientes (n).
    
    Retorna:
    - x: np.array conteniendo la solución del sistema.
    
    Lanza:
    - ValueError: Si el determinante de A es cero, indicando que el sistema no tiene solución única.
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    
    n = len(b)
    D = np.linalg.det(A)  # Determinante de A

    if np.isclose(D, 0):
        raise ValueError("El determinante de A es cero. El sistema no tiene solución única.")

    x = np.zeros(n)

    for k in range(n):
        Ak = A.copy()
        Ak[:, k] = b  # Reemplaza la columna k por el vector b
        Dk = np.linalg.det(Ak)
        x[k] = Dk / D

    return x