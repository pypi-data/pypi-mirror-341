import numpy as np

def gauss_eliminacion(coeficientes, terminos_ind):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Gauss con pivoteo parcial.

    Parámetros:
    - coeficientes: matriz de coeficientes (lista de listas o np.array)
    - terminos_ind: vector de términos independientes (lista o np.array)

    Retorna:
    - numpy array con la solución del sistema
    """
    A = np.array(coeficientes, dtype=float)
    b = np.array(terminos_ind, dtype=float).reshape(-1, 1)
    matriz = np.hstack([A, b])
    n = len(b)

    for i in range(n):
        max_fila = i + np.argmax(np.abs(matriz[i:, i]))
        matriz[[i, max_fila]] = matriz[[max_fila, i]]

        if abs(matriz[i, i]) < 1e-12:
            raise ValueError(f"Pivote casi cero en fila {i}, posible matriz singular.")

        for j in range(i + 1, n):
            factor = matriz[j, i] / matriz[i, i]
            matriz[j, i:] -= factor * matriz[i, i:]

    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        suma = np.dot(matriz[i, i + 1:n], x[i + 1:n])
        x[i] = (matriz[i, -1] - suma) / matriz[i, i]

    return x

