import numpy as np

def jacobi_iterativo(matriz_coeficientes, terminos_independientes, tolerancia=1e-10, max_iter=1000):
    """
    Resuelve un sistema de ecuaciones lineales utilizando el método iterativo de Jacobi.
    
    Parámetros:
      matriz_coeficientes: Matriz (n x n) de coeficientes.
      terminos_independientes: Vector (n) de términos independientes.
      tolerancia: Diferencia máxima permitida entre iteraciones.
      max_iter: Número máximo de iteraciones.
      
    Retorna:
      solucion: Vector solución (array de NumPy).
    """
    A = np.array(matriz_coeficientes, dtype=float)
    b = np.array(terminos_independientes, dtype=float)
    n = len(b)
    
    solucion = np.zeros(n)
    nueva_solucion = np.zeros(n)
    
    print("Método de Jacobi")
    print("Condición de convergencia: diferencia máxima < {:.4e}".format(tolerancia))
    
    for iteracion in range(1, max_iter + 1):
        print(f"\nIteración {iteracion}:")
        for i in range(n):
            suma = 0
            for j in range(n):
                if i != j:
                    suma += A[i, j] * solucion[j]
            nueva_solucion[i] = (b[i] - suma) / A[i, i]
            print(f"  Cálculo de x[{i}]: ({b[i]:.4f} - {suma:.4f}) / {A[i, i]:.4f} = {nueva_solucion[i]:.6f}")
        
        diferencia = np.linalg.norm(nueva_solucion - solucion, ord=np.inf)
        print(f"  Diferencia máxima en esta iteración: {diferencia:.6e}")
        
        if diferencia < tolerancia:
            print(f"\nConvergencia alcanzada en {iteracion} iteraciones.")
            return nueva_solucion
        
        solucion = nueva_solucion.copy()
    
    print("\nNo se alcanzó la convergencia en el número máximo de iteraciones.")
    return nueva_solucion
