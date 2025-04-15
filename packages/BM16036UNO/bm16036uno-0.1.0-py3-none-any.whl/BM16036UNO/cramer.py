import numpy as np

def metodo_cramer(matriz_coeficientes, terminos_independientes):
    """
    Resuelve un sistema de ecuaciones lineales utilizando el método de Cramer.
    
    Parámetros:
      matriz_coeficientes: Lista o array (n x n) de coeficientes.
      terminos_independientes: Lista o array (n) de términos independientes.
      
    Retorna:
      solucion: Vector solución o No si el sistema no tiene solución única.
    """
    A = np.array(matriz_coeficientes, dtype=float)
    b = np.array(terminos_independientes, dtype=float)
    n = len(b)
    
    determinante_principal = np.linalg.det(A)
    print("Determinante de la matriz de coeficientes (Δ): {:.4f}".format(determinante_principal))
    
    if np.isclose(determinante_principal, 0):
        print("El sistema no tiene solución única, ya que el determinante es cero (Δ = 0).")
        return None
    
    solucion = np.zeros(n)
    for i in range(n):
        A_modificada = A.copy()
        A_modificada[:, i] = b
        determinante_i = np.linalg.det(A_modificada)
        solucion[i] = determinante_i / determinante_principal
        
        print(f"\nPara la variable x{i+1}:")
        print("Matriz modificada (columna {0} reemplazada por b):".format(i+1))
        print(A_modificada)
        print("Determinante de la matriz modificada (Δ{0}): {1:.4f}".format(i+1, determinante_i))
        print(f"x{i+1} = Δ{i+1} / Δ = {determinante_i:.4f} / {determinante_principal:.4f} = {solucion[i]:.4f}")
    
    print("\nVector solución final:")
    print(solucion)
    return solucion
