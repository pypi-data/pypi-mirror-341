import numpy as np

def gauss_seidel(A, b, tol=1e-10, max_iter=1000):
    """
    Método de Gauss-Seidel para resolver sistemas lineales, mostrando el proceso paso a paso.

    Parámetros:
    - A: matriz de coeficientes (numpy array)
    - b: vector de términos independientes (numpy array)
    - tol: tolerancia para el criterio de convergencia
    - max_iter: número máximo de iteraciones

    Retorna:
    - Aproximación de la solución como numpy array
    """
    n = len(b)
    x = np.zeros(n)

    print("\n==== Método de Gauss-Seidel ====")
    print(f"Condición de parada: diferencia < {tol}\n")

    for k in range(1, max_iter + 1):
        x_prev = x.copy()
        print(f"Iteración {k}:")
        for i in range(n):
            suma = sum(A[i, j] * x[j] for j in range(n) if j != i)
            x[i] = (b[i] - suma) / A[i, i]
            print(f"x[{i}] = ({b[i]:.4f} - {suma:.4f}) / {A[i,i]:.4f} = {x[i]:.6f}")

        diff = np.linalg.norm(x - x_prev)
        print(f"Diferencia con la iteración anterior: {diff:.6e}\n")

        if diff < tol:
            print(f"Convergencia alcanzada en {k} iteraciones.")
            return x

    print("No se alcanzó convergencia en el número máximo de iteraciones.")
    return x

