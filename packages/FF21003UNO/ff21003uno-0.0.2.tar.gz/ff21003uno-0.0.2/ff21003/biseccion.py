def bisection(func, a, b, tol=1e-10, max=1000):
    """
    Resuelve una ecuación no lineal usando el método de bisección.
    
    Parámetros:
    func (function): Función cuya raíz se desea encontrar.
    a (float): Extremo izquierdo del intervalo.
    b (float): Extremo derecho del intervalo.
    tol (float): Tolerancia para la convergencia.
    max (int): Número máximo de iteraciones.
    
    """
    if func(a) * func(b) >= 0:
        raise ValueError("Los valores en los extremos del intervalo deben tener signos opuestos.")
    
    for _ in range(max):
        c = (a + b) / 2
        if abs(func(c)) < tol:
            return c
        elif func(c) * func(a) < 0:
            b = c
        else:
            a = c
    return c

# Ejemplo de uso:
if __name__ == "__main__":
    func = lambda x: x**2 - 4  
    raiz = bisection(func, 1, 3)
    print("Raíz encontrada usando el método de Bisección:", raiz)
