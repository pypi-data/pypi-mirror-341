import numpy as np

def imprimir_matriz_simple(matriz, nombre="Matriz"):
    print(f"\n{nombre}:")
    for fila in matriz:
        print("  ".join(f"{val:8.3f}" for val in fila))

def metodo_cramer(A, b):
    """
    Resuelve un sistema de ecuaciones lineales 3x3 usando el método de Cramer.

    Parámetros:
    - A: matriz de coeficientes (3x3)
    - b: vector de términos independientes (3x1)

    Retorna:
    - Lista con las soluciones [x, y, z] o None si no hay solución única.
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    print("\n==== Método de Cramer ====")
    print("\nPaso 1: Matriz de coeficientes (A) y vector de términos independientes (b):")
    imprimir_matriz_simple(A, "A")
    print(f"\nb = {b}")

    # Determinante principal Δ
    delta = np.linalg.det(A)
    print(f"\nPaso 2: Calculamos el determinante de la matriz A (Δ): {delta:.3f}")

    if np.isclose(delta, 0):
        print("El sistema no tiene solución única (Δ = 0).")
        return None

    soluciones = []
    variables = ['x', 'y', 'z']
    for i in range(3):
        A_mod = A.copy()
        A_mod[:, i] = b
        delta_i = np.linalg.det(A_mod)
        print(f"\nPaso 3: Reemplazamos la columna {i} por el vector b y calculamos Δ{variables[i]}:")
        imprimir_matriz_simple(A_mod, f"A con columna {variables[i]} reemplazada")
        print(f"Δ{variables[i]} = {delta_i:.3f}")
        soluciones.append(delta_i / delta)
        print(f"{variables[i]} = Δ{variables[i]} / Δ = {delta_i:.3f} / {delta:.3f} = {soluciones[-1]:.3f}")

    return soluciones


