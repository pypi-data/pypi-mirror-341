import math

def biseccion(f,a,b,tol=1e-6,max_iter=1000):
    """
    Resuelve ecuaciones lineales, encontrando la raiz. f(x) = 0 en [a,b]
    Parametros:
        f: funcion a evaluar
        a: valor menor
        b: valor mayor
        tol: tolerancia
        max_iter: maximo de iteraciones
    Retorna:
        float: Raiz aproximada
        int: Numero de iteraciones.

    """
    
    if(f(a)*f(b)) >= 0:
        raise ValueError("Error, la funcion no cambia de signo en [a,b]")
    iteraciones = 0
    while (b-a)/2 > tol and iteraciones < max_iter:
        c = (a + b) / 2
        if (f(c) == 0):
            return c, iteraciones
        elif f(a) * f(c) < 0:
            b = c #la raiz se encuentra entre a y c
        else:
            a = c #la raiz se encuentra entre c y b
        iteraciones += 1

    return (a + b) / 2, iteraciones


