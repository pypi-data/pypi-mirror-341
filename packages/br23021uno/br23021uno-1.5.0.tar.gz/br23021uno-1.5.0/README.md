# BR23021UNO 
**Autor:** [Joyser Leonel Barrera Romero]  
**Versión:** 1.0.0  
**Descripción:** Librería para resolver sistemas de ecuaciones lineales y no lineales utilizando métodos numéricos.
Permite resolver ecuaciones usando los siguientes métodos : Eliminación de Gauss, Gauss-Jordan, Regla de Crammer,Descomposición LU, Jacobi, Gauss-Seidel y Bisección.   

## Instalación  
Para instalar la librería, usa el siguiente comando en tu terminal:  
```bash 
pip install BR23021UNO 
```

## Dependencias
Para que la librería funcione correctamente, asegúrate de instalar las siguiente dependencia:
```bash 
pip install numpy 
```
## Ejemplos de uso
    
### biseccion:
```py
            #import math
            # Definir la función que queremos evaluar
            funcion = lambda x: x**4 + 0.5*(x**3) - 2*x - 5
            #Llamar a la funcion
            raiz, iteraciones = biseccion(funcion,100,0)

            # Mostrar el resultado con 6 cifras significativas
            print(f"Raiz de funcion por biseccion es igual a {raiz:.6f}, encontrada en un total de {iteraciones} iteraciones.")

            #Salida esperada: 
            #Raiz de funcion por biseccion es igual a 50.000000, encontrada en un total de 0 iteraciones.
```
### crammer:
```py

            # Matriz de coeficientes (A) y vector de términos independientes (b)
            A = [
                [2, 1, 3],
                [3, -2, -1],
                [1, 3, 2]
            ]

            b = [1, 0, 5]

            # Resolver el sistema Ax = b usando la regla de Cramer
            solucion = cramer(A, b)

            print(f"Solución del sistema: {solucion}")

            #Resultado esperado : Solución del sistema: [ 1.  2. -1.]
```
### descomposicion_lu:

```py
            # Definir la matriz de coeficientes (A) y el vector de términos independientes (b)
            A = np.array([
                [25, 5, 1],
                [64,  8, 1],
                [144,  12, 1]
            ], dtype=float)

            b = np.array([106.8, 177.2, 279.2], dtype=float)

            # Resolver el sistema Ax = b usando la descomposición LU
            solucion = lu_solve(A, b)

            print("Solución del sistema:", solucion)
            ##Resultado esperado: Solución del sistema: [ 0.29047619 19.69047619  1.08571429]
```
### eliminacion_gauss
```py
    # Definir la matriz de coeficientes A y el vector de términos independientes b
    A = np.array([
    [2, 3, 1],
    [1, 1, 2],
    [1, -1, -1]
    ], dtype=float)

    b = np.array([0, 1, -1], dtype=float)

    # Resolver el sistema Ax = b usando el método de eliminación de Gauss
    solution = gauss_elimination(A, b)

    print(f"Solución del sistema: {solution}")
    ##Salida esperada: Solución del sistema: [-0.33333333 -0.          0.66666667]
```
### gauss_jordan
```py
    # Definir la matriz de coeficientes del sistema Ax = b
    coefficients = [
        [1, 1, -1],
        [1, -2, 3],
        [2, -1, 3]
    ]

    # Definir el vector de términos independientes
    ind_terms = [2, 0, 3]

    # Resolver el sistema mediante el método de Gauss-Jordan
    solution = gauss_jordan(coefficients, ind_terms)

    # Mostrar la solución del sistema
    print("Solución del sistema:", solution)
    #Resultado esperado: Solución del sistema: [1. 2. 1.]
```
### gauss_seidel
```py
    #Definir la matriz
    A = np.array([
        [9, 2, -1],
        [7, 8, 5],
        [3, 4, -10]
    ], dtype=float)

    b = np.array([-2, 3, 6], dtype=float)

    # Resolver el sistema usando el método de Gauss-Seidel
    solution = gauss_seidel(A, b)

    # Mostrar la solución encontrada
    print("La solución aproximada del sistema es:", solution)

    #Resultado esperado: La solución aproximada del sistema es: [-0.48501362  1.01226158 -0.34059946]

```
### jacobi
```py
    #Definimos la matriz
    A = np.array([
        [2, -1, 1],
        [1, 2, -1],
        [1, 1, 1]
    ], dtype=float)

    b = np.array([7, 6, 12], dtype=float)

    # Resolver el sistema Ax = b usando el método de Jacobi
    solution = jacobi(A, b)

    # Mostrar la solución aproximada 
    print("La solución aproximada del sistema es:", solution)

    #Solucion esperada: La solución aproximada del sistema es: [3. 4. 5.]
```
## Contacto  
Email: **br23021@ues.edu.sv**  
GitHub: (https://github.com/JoyserB/BR23021UNO)  
Universidad de El Salvador  
