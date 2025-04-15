import numpy as np

def descomposicion_lu(matriz_coeficientes):
    """
    Realiza la descomposición LU de una matriz cuadrada A, de modo que A = L * U,
    donde L es una matriz triangular inferior con 1 en su diagonal y U es una matriz triangular superior.
    
    Parámetros:
      matriz_coeficientes: Lista de listas o array (n x n) con los coeficientes de A.
      
    Retorna:
      L: Matriz triangular inferior.
      U: Matriz triangular superior.
    """
    A = np.array(matriz_coeficientes, dtype=float)
    n = A.shape[0]
    
    L = np.eye(n, dtype=float)
    U = A.copy()
    
    print("Matriz A inicial:")
    print(A)
    
    for k in range(n):
        if np.isclose(U[k, k], 0):
            raise ValueError(f"Pivote cero detectado en U[{k},{k}]. La descomposición LU falla sin pivoteo.")
        
        for i in range(k+1, n):
            factor = U[i, k] / U[k, k]
            L[i, k] = factor
            print(f"\nCalculamos el factor para L[{i},{k}] = {factor:.4f}")
            U[i, k:] = U[i, k:] - factor * U[k, k:]
            print(f"Actualizando la fila {i} de U:")
            print(U[i, :])
    
    print("\nMatriz L (Triangular Inferior):")
    print(L)
    print("\nMatriz U (Triangular Superior):")
    print(U)
    
    return L, U
