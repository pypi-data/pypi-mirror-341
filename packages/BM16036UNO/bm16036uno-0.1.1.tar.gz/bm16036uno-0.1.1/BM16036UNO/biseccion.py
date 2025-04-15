import numpy as np

def biseccion_paso_a_paso(f, a, b, tol=1e-6, max_iter=100):
    """
    Método de bisección para encontrar una raíz de f en el intervalo [a, b],
    mostrando el proceso paso a paso.

    Parámetros:
    - f: función a evaluar
    - a, b: extremos del intervalo
    - tol: tolerancia aceptable
    - max_iter: número máximo de iteraciones

    Retorna:
    - La raíz aproximada si converge, None si no aplica el método
    """
    print("\n==== Método de la Bisección ====")
    print(f"Intervalo inicial: [{a}, {b}]")
    print(f"Tolerancia: {tol}")

    if f(a) * f(b) >= 0:
        print("El método de bisección no puede aplicarse: f(a) y f(b) deben tener signos opuestos.")
        return None

    for i in range(1, max_iter + 1):
        c = (a + b) / 2
        fc = f(c)
        print(f"\nIteración {i}:")
        print(f"a = {a:.6f}, b = {b:.6f}, c = {c:.6f}, f(c) = {fc:.6e}")

        if abs(fc) < tol or (b - a) / 2 < tol:
            print(f"\nConvergencia alcanzada en la iteración {i}. Raíz aproximada: {c:.6f}")
            return c

        if f(a) * fc < 0:
            b = c
        else:
            a = c

    print("\nNo se alcanzó la convergencia en el número máximo de iteraciones.")
    return (a + b) / 2


