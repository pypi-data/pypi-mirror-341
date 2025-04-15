import numpy as np

def gauss_jordan(matriz_coeficientes, terminos_independientes):
    """
    Resuelve un sistema de ecuaciones lineales utilizando el método de Gauss-Jordan.
    Transforma la matriz aumentada en la forma [I | X], donde I es la matriz identidad y X es el vector solución.
    
    Parámetros:
      matriz_coeficientes: Lista de listas o array (n x n) con los coeficientes.
      terminos_independientes: Lista o array (n) de términos independientes.
      
    Retorna:
      solucion: Vector solución.
    """
    A = np.array(matriz_coeficientes, dtype=float)
    b = np.array(terminos_independientes, dtype=float)
    n = len(b)
    
    matriz_aumentada = np.hstack((A, b.reshape(n, 1)))
    print("Matriz Aumentada Inicial:")
    print(matriz_aumentada)
    
    for i in range(n):
        indice_maximo = np.argmax(np.abs(matriz_aumentada[i:, i])) + i
        
        if np.isclose(matriz_aumentada[indice_maximo, i], 0):
            raise ValueError("La matriz es singular o casi singular; el sistema no tiene solución única.")
        
        if indice_maximo != i:
            print(f"\nIntercambiamos la fila {i} con la fila {indice_maximo} para optimizar el pivote.")
            matriz_aumentada[[i, indice_maximo]] = matriz_aumentada[[indice_maximo, i]]
            print("Matriz después del intercambio:")
            print(matriz_aumentada)
        
        pivote = matriz_aumentada[i, i]
        print(f"\nNormalizando la fila {i}; pivote = {pivote:.4f}")
        matriz_aumentada[i] = matriz_aumentada[i] / pivote
        print("Matriz después de normalizar la fila:")
        print(matriz_aumentada)
        
        for j in range(n):
            if j != i:
                factor = matriz_aumentada[j, i]
                print(f"\nEliminando el elemento en la fila {j}, columna {i} usando factor = {factor:.4f}")
                matriz_aumentada[j] -= factor * matriz_aumentada[i]
                print(f"Matriz después de ajustar la fila {j}:")
                print(matriz_aumentada)
    
    solucion = matriz_aumentada[:, -1]
    print("\nMatriz Aumentada final [I | X]:")
    print(matriz_aumentada)
    print("\nVector solución final:")
    print(solucion)
    return solucion
