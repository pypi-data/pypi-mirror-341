import numpy as np

def jacobi(A, b, tol=1e-10, max_iter=1000):
    """
    Resuelve sistemas de ecuaciones lineales Ax = b usando el metodo de Jacobi

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
    x_new = np.zeros(n)


    for k in range(max_iter):
        for i in range(n):
            x_new[i]= (b[i] - sum(A[i,j] * x[j] for j in range(n) if j != i))/A[i,i]

        if np.linalg.norm(x_new - x) < tol:
            print(f"Total de iteraciones necesitadas: {k}")
            return x_new
        
        x = x_new.copy()
    
    print(f"No se pudo converger en {max_iter} iteraciones.")
    return x
