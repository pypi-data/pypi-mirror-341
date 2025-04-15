def biseccion(f, limite_inferior, limite_superior, tolerancia=1e-6, max_iter=1000):
    """
    Resuelve la ecuación f(x) = 0 en el intervalo [limite_inferior, limite_superior]
    utilizando el método de bisección.

    Parámetros:
      f: Función a evaluar.
      limite_inferior: Valor inferior del intervalo.
      limite_superior: Valor superior del intervalo.
      tolerancia: Precisión requerida.
      max_iter: Número máximo de iteraciones.
      
    Retorna:
      (raiz, iteraciones): Tupla con la raíz aproximada y el número de iteraciones utilizadas.
    """
    if f(limite_inferior) * f(limite_superior) >= 0:
        raise ValueError("La función no cambia de signo en el intervalo dado.")
    
    print("Método de Bisección")
    print(f"Intervalo inicial: [{limite_inferior}, {limite_superior}]")
    print(f"Tolerancia: {tolerancia}\n")
    
    iteraciones = 0
    while (limite_superior - limite_inferior) / 2 > tolerancia and iteraciones < max_iter:
        punto_medio = (limite_inferior + limite_superior) / 2
        valor_f_medio = f(punto_medio)
        iteraciones += 1
        
        print(f"Iteración {iteraciones}:")
        print(f"  Límite inferior = {limite_inferior:.6f}")
        print(f"  Límite superior = {limite_superior:.6f}")
        print(f"  Punto medio    = {punto_medio:.6f}")
        print(f"  f(punto_medio) = {valor_f_medio:.6e}\n")
        
        if abs(valor_f_medio) < tolerancia:
            print("Convergencia alcanzada: f(punto_medio) es suficientemente cercano a cero.")
            return punto_medio, iteraciones
        
        if f(limite_inferior) * valor_f_medio < 0:
            limite_superior = punto_medio
        else:
            limite_inferior = punto_medio
    
    print("No se alcanzó la tolerancia requerida en el número máximo de iteraciones.")
    raiz = (limite_inferior + limite_superior) / 2
    return raiz, iteraciones
