import numpy as np

def imprimir_matriz(matriz, paso):
    print(f"\nPaso {paso}: Estado actual de la matriz aumentada")
    for fila in matriz:
        print("  ".join(f"{elem:8.3f}" for elem in fila))

def gauss_jordan(coeficientes, terminos_ind):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Gauss-Jordan con pivoteo parcial.

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
    paso = 1
    imprimir_matriz(matriz, paso)

    # Eliminación Gauss-Jordan
    for i in range(n):
        paso += 1
        # Pivoteo parcial
        max_fila = i + np.argmax(np.abs(matriz[i:, i]))
        matriz[[i, max_fila]] = matriz[[max_fila, i]]

        # Normaliza la fila del pivote
        pivote = matriz[i, i]
        if abs(pivote) < 1e-12:
            raise ValueError(f"Pivote casi cero en fila {i}, posible matriz singular.")
        matriz[i] = matriz[i] / pivote
        print(f"\nNormalizamos la fila {i} dividiendo por el pivote {pivote:.3f}")
        imprimir_matriz(matriz, paso)

        # Hacemos ceros en todas las demás filas (arriba y abajo)
        for j in range(n):
            if j != i:
                factor = matriz[j, i]
                matriz[j] -= factor * matriz[i]
                print(f"\nRestamos {factor:.3f} * fila {i} a fila {j} para hacer 0 en posición ({j}, {i})")
                paso += 1
                imprimir_matriz(matriz, paso)

    # La última columna contiene la solución
    solucion = matriz[:, -1]
    print("\nSistema reducido. Solución encontrada:")
    for idx, val in enumerate(solucion):
        print(f"x{idx} = {val:.6f}")
    return solucion
