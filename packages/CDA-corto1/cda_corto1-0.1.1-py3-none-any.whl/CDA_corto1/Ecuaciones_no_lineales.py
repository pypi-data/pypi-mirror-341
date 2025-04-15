import numpy as np

def bisection(f, a, b, tol=1e-6, max_iter=100):
    """
    Encuentra una raiz de f(x) = 0 en el intervalo [a, b] usando el metodo de bisección
    
    Args:
        f: Funcion a encontrar la raiz
        a, b: Extremos del intervalo
        tol: Tolerancia para la convergencia
        max_iter: Numero maximo de iteraciones
    
    Returns:
        c: Aproximacion de la raiz
    """
    if f(a) * f(b) >= 0:
        raise ValueError("La funcion debe cambiar de signo en el intervalo [a, b]")
    
    for _ in range(max_iter):
        c = (a + b) / 2
        if abs(f(c)) < tol:
            return c
        
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    
    return (a + b) / 2