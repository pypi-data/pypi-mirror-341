"""
Paquete IA22001UNO - Métodos numéricos para sistemas de ecuaciones

Este paquete contiene implementaciones de:
- Eliminación de Gauss
- Gauss-Jordan
- Regla de Cramer
- Descomposición LU
- Método de Jacobi
- Método de Gauss-Seidel
- Método de Bisección
"""

from .metodos import (
    eliminacion_gauss,
    gauss_jordan,
    crammer,
    descomposicion_lu,
    jacobi,
    gauss_seidel,
    biseccion
)

__all__ = [
    'eliminacion_gauss',
    'gauss_jordan',
    'crammer',
    'descomposicion_lu',
    'jacobi',
    'gauss_seidel',
    'biseccion'
]

__version__ = '0.1.0'