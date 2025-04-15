# sistema_solver/__init__.py

from .lineal import gauss_eliminacion, gauss_jordan, cramer, descomposicion_lu, jacobi, gauss_seidel
from .no_lineal import biseccion

__all__ = [
    'gauss_eliminacion',
    'gauss_jordan',
    'cramer',
    'descomposicion_lu',
    'jacobi',
    'gauss_seidel',
    'biseccion'
]
