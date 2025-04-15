import numpy as np

def imprimir_matriz(matriz, nombre):
    print(f"\n{name_format(nombre)}:")
    for fila in matriz:
        print("  ".join(f"{val:8.3f}" for val in fila))

def name_format(nombre):
    return f"{nombre}".ljust(15)

def descomposicion_lu(A, b):
    """
    Resuelve un sistema Ax = b usando descomposición LU (sin pivoteo).

    Parámetros:
    - A: matriz de coeficientes (n x n)
    - b: vector de términos independientes

    Retorna:
    - Vector solución x
    """
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = A.shape[0]

    L = np.zeros((n, n))
    U = np.zeros((n, n))

    print("\n==== Descomposición LU ====")
    print("\nPaso 1: Iniciamos la descomposición A = LU")

    for i in range(n):
        # Llenar U
        for j in range(i, n):
            suma = sum(L[i][k] * U[k][j] for k in range(i))
            U[i][j] = A[i][j] - suma

        # Llenar L
        for j in range(i, n):
            if i == j:
                L[j][i] = 1
            else:
                suma = sum(L[j][k] * U[k][i] for k in range(i))
                if abs(U[i][i]) < 1e-12:
                    raise ValueError(f"División por cero al construir L, pivote U[{i}][{i}] = 0")
                L[j][i] = (A[j][i] - suma) / U[i][i]

    imprimir_matriz(L, "Matriz L")
    imprimir_matriz(U, "Matriz U")

    print("\nPaso 2: Resolver Ly = b (sustitución hacia adelante)")
    y = np.zeros(n)
    for i in range(n):
        y[i] = (b[i] - sum(L[i][k] * y[k] for k in range(i)))
        print(f"y[{i}] = {y[i]:.6f}")

    print("\nPaso 3: Resolver Ux = y (sustitución hacia atrás)")
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - sum(U[i][k] * x[k] for k in range(i + 1, n))) / U[i][i]
        print(f"x[{i}] = {x[i]:.6f}")

    return x

