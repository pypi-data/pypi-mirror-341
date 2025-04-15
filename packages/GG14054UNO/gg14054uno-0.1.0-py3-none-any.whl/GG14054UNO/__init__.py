"""
GG14054UNO: Librería para resolver sistemas de ecuaciones lineales y no lineales.

Métodos implementados:
- Eliminación de Gauss
- Gauss-Jordan
- Cramer
- Descomposición LU
- Jacobi
- Gauss-Seidel
- Bisección
"""

from .linear_systems import (
    gauss_elimination,
    gauss_jordan,
    cramer,
    lu_decomposition,
    jacobi,
    gauss_seidel
)
from .nonlinear_systems import bisection

__version__ = "0.1.0"