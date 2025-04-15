import numpy as np

def jacobi_paso_a_paso(A, b, tol=1e-10, max_iter=1000):
    """
    Método de Jacobi para resolver sistemas lineales, mostrando el proceso paso a paso.

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
    x_new = np.zeros(n)

    print("\n==== Método de Jacobi ====")
    print(f"Condición de parada: diferencia < {tol}\n")

    for k in range(1, max_iter + 1):
        print(f"Iteración {k}:")
        for i in range(n):
            suma = sum(A[i, j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - suma) / A[i, i]
            print(f"x[{i}] = ({b[i]:.4f} - {suma:.4f}) / {A[i,i]:.4f} = {x_new[i]:.6f}")

        diff = np.linalg.norm(x_new - x)
        print(f"Diferencia con la iteración anterior: {diff:.6e}\n")

        if diff < tol:
            print(f"Convergencia alcanzada en {k} iteraciones.")
            return x_new

        x = x_new.copy()

    print("No se alcanzó convergencia en el número máximo de iteraciones.")
    return x_new


