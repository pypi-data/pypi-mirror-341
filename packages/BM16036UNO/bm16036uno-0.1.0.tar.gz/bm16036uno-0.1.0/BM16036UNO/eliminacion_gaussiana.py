import numpy as np

def eliminacion_gaussiana(matriz_coeficientes, terminos_independientes):
    """
    Resuelve un sistema de ecuaciones lineales utilizando el método de Eliminación de Gauss.
    
    Parámetros:
      matriz_coeficientes: Lista de listas o array (n x n) con los coeficientes del sistema.
      terminos_independientes: Lista o array (n) con los términos independientes.
      
    Retorna:
      solucion: Vector solución.
    """
    A = np.array(matriz_coeficientes, dtype=float)
    b = np.array(terminos_independientes, dtype=float)
    numero_ecuaciones = len(b)
    
    # Construir la matriz aumentada [A | b].
    matriz_aumentada = np.hstack((A, b.reshape(numero_ecuaciones, 1)))
    print("Matriz Aumentada Inicial:")
    print(matriz_aumentada)
    
    # Eliminación hacia adelante.
    for indice_pivote in range(numero_ecuaciones):
        indice_maximo = np.argmax(np.abs(matriz_aumentada[indice_pivote:, indice_pivote])) + indice_pivote
        
        if np.isclose(matriz_aumentada[indice_maximo, indice_pivote], 0):
            raise ValueError("La matriz es singular o casi singular; no se puede encontrar una solución única.")
        
        if indice_maximo != indice_pivote:
            print(f"\nIntercambiamos la fila {indice_pivote} con la fila {indice_maximo} para usar el mejor pivote.")
            matriz_aumentada[[indice_pivote, indice_maximo]] = matriz_aumentada[[indice_maximo, indice_pivote]]
            print("Matriz tras el intercambio:")
            print(matriz_aumentada)
        
        for fila in range(indice_pivote + 1, numero_ecuaciones):
            factor = matriz_aumentada[fila, indice_pivote] / matriz_aumentada[indice_pivote, indice_pivote]
            print(f"\nEliminando el elemento en la fila {fila}, columna {indice_pivote} usando factor = {factor:.4f}.")
            matriz_aumentada[fila, indice_pivote:] -= factor * matriz_aumentada[indice_pivote, indice_pivote:]
            print("Matriz actualizada:")
            print(matriz_aumentada)
    
    # Sustitución hacia atrás.
    solucion = np.zeros(numero_ecuaciones)
    for i in range(numero_ecuaciones - 1, -1, -1):
        suma_conocida = np.dot(matriz_aumentada[i, i+1:numero_ecuaciones], solucion[i+1:numero_ecuaciones])
        solucion[i] = (matriz_aumentada[i, -1] - suma_conocida) / matriz_aumentada[i, i]
        print(f"\nSustitución hacia atrás, fila {i}:")
        print(f"Suma de términos conocidos = {suma_conocida:.4f}  =>  solucion[{i}] = {solucion[i]:.4f}")
    
    print("\nVector solución final:")
    print(solucion)
    return solucion
