import numpy as np

def gauss_seidel(A, b, tol=1e-10, max_iter=1000):
    """
    Resuelve sistemas de ecuaciones lineales Ax = b usando el metodo de gauss-seidel

    Parametros:
        A: Matriz de coeficientes.
        b: Vector de terminos independientes.
        tol: Tolerancia para la convergencia.
        max_iter: Maximo numero de iteraciones.

    Retorna:
        x: Solucion aproximada.
    """

    n = len(b)
    x = np.zeros(n)

    for k in range(max_iter):
        x_prev = x.copy()

        for i in range(n):
            x[i]= (b[i] - sum(A[i,j] * x[j] for j in range(n) if j != i)) / A[i,i]

        if np.linalg.norm(x - x_prev) < tol:   #verificamos la convergencia
            return x
        
    print(f"No se pudo converger en {max_iter} iteraciones.")
    return x



