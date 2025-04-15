import numpy as np

def descomposicion_lu(A):
    """
    Realiza la descomposición LU de una matriz cuadrada A usando el algoritmo.
    
    Parametros:
      A (np.array): Matriz de coeficientes (n x n).

    Retorna:
      L (np.array): Matriz triangular inferior con 1's en la diagonal.
      U (np.array): Matriz triangular superior.
    
    Nota: Se asume que A es no singular y que no se requiere pivoteo.
    """
    A = A.astype(float)
    n = A.shape[0]
    
    # Inicializamos L y U
    L = np.eye(n, dtype=float)
    U = np.zeros((n, n), dtype=float)
    
    # Algoritmo de Doolittle
    for i in range(n):
        # Calcular la fila i de U
        for j in range(i, n):
            sum_u = 0.0
            for k in range(i):
                sum_u += L[i, k] * U[k, j]
            U[i, j] = A[i, j] - sum_u

        # Calcular la columna i de L (para elementos debajo de la diagonal)
        for j in range(i + 1, n):
            sum_l = 0.0
            for k in range(i):
                sum_l += L[j, k] * U[k, i]
            L[j, i] = (A[j, i] - sum_l) / U[i, i]
    
    return L, U

def lu_solve(A, b):
    """
    Resuelve el sistema Ax = b usando la descomposición LU.
    
    Parámetros:
      A (np.array): Matriz de coeficientes (n x n).
      b (np.array): Vector de términos independientes (n,).
      
    Retorna:
      x (np.array): Solución del sistema.
    """
    L, U = descomposicion_lu(A)
    n = A.shape[0]
    
    # Resolución del sistema L y = b mediante sustitución progresiva:
    y = np.zeros(n, dtype=float)
    for i in range(n):
        sum_y = 0.0
        for j in range(i):
            sum_y += L[i, j] * y[j]
        y[i] = b[i] - sum_y
        
    # Resolución del sistema U x = y mediante sustitución regresiva:
    x = np.zeros(n, dtype=float)
    for i in range(n - 1, -1, -1):
        sum_x = 0.0
        for j in range(i + 1, n):
            sum_x += U[i, j] * x[j]
        x[i] = (y[i] - sum_x) / U[i, i]
        
    return x