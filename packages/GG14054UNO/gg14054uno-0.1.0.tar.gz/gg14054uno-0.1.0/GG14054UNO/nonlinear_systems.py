import numpy as np
from typing import Callable, Tuple, Union, List

def bisection(f: Callable[[float], float], a: float, b: float, tol: float = 1e-10, max_iter: int = 100) -> float:
    """
    Encuentra una raíz de una función utilizando el método de bisección.
    
    Args:
        f: Función para encontrar su raíz
        a: Límite inferior del intervalo
        b: Límite superior del intervalo
        tol: Tolerancia para convergencia
        max_iter: Número máximo de iteraciones
        
    Returns:
        Aproximación de la raíz
    """
    if f(a) * f(b) >= 0:
        raise ValueError("La función debe tener signos opuestos en los extremos del intervalo")
    
    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        
        if abs(fc) < tol:
            return c
        
        if f(a) * fc < 0:
            b = c
        else:
            a = c
        
        # También podemos verificar si el intervalo es suficientemente pequeño
        if abs(b - a) < tol:
            return c
    
    print(f"Advertencia: El método de bisección no convergió después de {max_iter} iteraciones")
    return (a + b) / 2

def solve_nonlinear_system_bisection(funcs: List[Callable], bounds: List[Tuple[float, float]], 
                                      tol: float = 1e-6, max_iter: int = 100) -> np.ndarray:
    """
    Resuelve un sistema de ecuaciones no lineales utilizando bisección para cada variable.
    Nota: Este método es simplificado y solo funciona en casos específicos.
    
    Args:
        funcs: Lista de funciones del sistema
        bounds: Lista de tuplas con los límites inferior y superior para cada variable
        tol: Tolerancia para convergencia
        max_iter: Número máximo de iteraciones
        
    Returns:
        Vector solución
    """
    n = len(funcs)
    if n != len(bounds):
        raise ValueError("El número de funciones debe ser igual al número de variables")
    
    x = np.zeros(n)
    
    # Este es un enfoque muy simplificado que asume que las variables son independientes
    # En la práctica, los sistemas no lineales requieren métodos más complejos como Newton-Raphson
    for i in range(n):
        a, b = bounds[i]
        x[i] = bisection(funcs[i], a, b, tol, max_iter)
    
    return x