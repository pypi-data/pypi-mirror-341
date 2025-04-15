
# GG14054UNO

Una librería Python para resolver sistemas de ecuaciones lineales y no lineales. Corto #1 de la materias CAD135.

## Instalación

```bash
pip install GG14054UNO
```

## Uso
## Sistemas lineales

```
import numpy as np
from GG14054UNO import gauss_elimination, gauss_jordan, cramer, lu_decomposition, jacobi, gauss_seidel

# Definir el sistema de ecuaciones Ax = b
A = np.array([[4, 1, -1], 
              [2, 7, 1], 
              [1, -3, 12]])
b = np.array([3, 19, 31])

# Resolver utilizando diferentes métodos
x1 = gauss_elimination(A, b)
x2 = gauss_jordan(A, b)
x3 = cramer(A, b)
x4 = lu_decomposition(A, b)
x5 = jacobi(A, b)
x6 = gauss_seidel(A, b)

print("Solución por eliminación de Gauss:", x1)
print("Solución por Gauss-Jordan:", x2)
print("Solución por regla de Cramer:", x3)
print("Solución por descomposición LU:", x4)
print("Solución por método de Jacobi:", x5)
print("Solución por método de Gauss-Seidel:", x6)

```

## Sistemas no lineales

```
from GG14054UNO import bisection

# Resolver una ecuación no lineal f(x) = 0
f = lambda x: x**2 - 4  # Ecuación x^2 - 4 = 0 (raíces en x = -2 y x = 2)

# Usar bisección para encontrar la raíz en el intervalo [1, 3]
root = bisection(f, 1, 3)
print("Raíz encontrada:", root)  # Debería ser aproximadamente 2

```

## Métodos Implementados

1. Eliminación de Gauss - Resuelve sistemas lineales mediante eliminación hacia adelante y sustitución hacia atrás.
2. Gauss-Jordan - Resuelve sistemas lineales reduciendo la matriz a su forma escalonada reducida.
3. Regla de Cramer - Utiliza determinantes para resolver sistemas lineales.
4. Descomposición LU - Factoriza la matriz en matrices triangulares inferior y superior.
5. Método de Jacobi - Método iterativo para sistemas lineales.
6. Método de Gauss-Seidel - Método iterativo con convergencia más rápida que Jacobi.
7. Método de Bisección - Encuentra raíces de ecuaciones no lineales.

## Requisitos

* NumPy
* SciPy

```
pip install numpy scipy

```