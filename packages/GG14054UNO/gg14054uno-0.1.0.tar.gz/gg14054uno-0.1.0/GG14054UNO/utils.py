import numpy as np
from typing import List, Tuple, Callable, Union

def check_system_consistency(A: np.ndarray, b: np.ndarray) -> str:
    """
    Verifica la consistencia de un sistema de ecuaciones lineales.
    
    Args:
        A: Matriz de coeficientes
        b: Vector de términos independientes
        
    Returns:
        Mensaje indicando si el sistema tiene solución única, infinitas soluciones o es inconsistente
    """
    # Calcular rangos
    rank_A = np.linalg.matrix_rank(A)
    augmented = np.column_stack((A, b))
    rank_aug = np.linalg.matrix_rank(augmented)
    
    n, m = A.shape
    
    if rank_A == rank_aug:
        if rank_A == m:
            return "El sistema tiene solución única."
        else:
            return "El sistema tiene infinitas soluciones."
    else:
        return "El sistema es inconsistente (no tiene solución)."

def residual_norm(A: np.ndarray, x: np.ndarray, b: np.ndarray) -> float:
    """
    Calcula la norma del residuo para evaluar la calidad de la solución.
    
    Args:
        A: Matriz de coeficientes
        x: Vector solución
        b: Vector de términos independientes
        
    Returns:
        Norma euclidiana del residuo ||Ax - b||
    """
    return np.linalg.norm(A.dot(x) - b)

def is_diagonally_dominant(A: np.ndarray) -> bool:
    """
    Verifica si una matriz es diagonalmente dominante.
    
    Args:
        A: Matriz a verificar
        
    Returns:
        True si la matriz es diagonalmente dominante, False en caso contrario
    """
    n = A.shape[0]
    for i in range(n):
        if abs(A[i, i]) <= sum(abs(A[i, j]) for j in range(n) if j != i):
            return False
    return True