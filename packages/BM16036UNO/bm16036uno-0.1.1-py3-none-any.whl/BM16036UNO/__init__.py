"""
Módulo principal de la librería BM16036UNO.

Se importan y exponen las funciones de resolución de sistemas de ecuaciones
lineales y no lineales implementadas en los siguientes módulos:
  - eliminacion_gaussiana.py
  - gauss_jordan.py
  - cramer.py
  - descomposicion_lu.py
  - jacobi.py
  - gauss_seidel.py
  - biseccion.py
"""

from .eliminacion_gaussiana import eliminacion_gaussiana
from .gauss_jordan import gauss_jordan
from .cramer import metodo_cramer
from .descomposicion_lu import descomposicion_lu
from .jacobi import jacobi_iterativo
from .gauss_seidel import gauss_seidel_iterativo
from .biseccion import biseccion

