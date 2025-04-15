import numpy as np

def gauss_seidel_iterativo(matriz_coeficientes, terminos_independientes, tolerancia=1e-10, max_iter=1000):
    """
    Resuelve un sistema de ecuaciones lineales utilizando el método iterativo de Gauss-Seidel.
    
    Parámetros:
      matriz_coeficientes: Matriz (n x n) de coeficientes.
      terminos_independientes: Vector (n) de términos independientes.
      tolerancia: Diferencia máxima permitida entre iteraciones.
      max_iter: Número máximo de iteraciones.
      
    Retorna:
      solucion: Vector solución.
    """
    A = np.array(matriz_coeficientes, dtype=float)
    b = np.array(terminos_independientes, dtype=float)
    n = len(b)
    
    solucion = np.zeros(n)
    
    print("Método de Gauss-Seidel")
    print("Condición de convergencia: diferencia máxima < {:.4e}".format(tolerancia))
    
    for iteracion in range(1, max_iter + 1):
        solucion_prev = solucion.copy()
        print(f"\nIteración {iteracion}:")
        for i in range(n):
            suma = 0
            for j in range(n):
                if j != i:
                    suma += A[i, j] * solucion[j]
            solucion[i] = (b[i] - suma) / A[i, i]
            print(f"  Calculamos x[{i}]: ({b[i]:.4f} - {suma:.4f}) / {A[i, i]:.4f} = {solucion[i]:.6f}")
        
        diferencia = np.linalg.norm(solucion - solucion_prev, ord=np.inf)
        print(f"  Diferencia máxima entre iteraciones: {diferencia:.6e}")
        
        if diferencia < tolerancia:
            print(f"\nConvergencia alcanzada en {iteracion} iteraciones.")
            return solucion
    
    print("\nNo se alcanzó la convergencia en el número máximo de iteraciones.")
    return solucion
