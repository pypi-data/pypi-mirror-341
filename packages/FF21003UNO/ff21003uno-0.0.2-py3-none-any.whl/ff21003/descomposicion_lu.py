import numpy as np
from scipy.linalg import lu

def descomposicion_lu(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando descomposición LU.
    
    Parámetros:
    A (numpy.ndarray): Matriz de coeficientes.
    b (numpy.ndarray): Vector de constantes.

    """
    P, L, U = lu(A)
    y = np.linalg.solve(L, b)
    x = np.linalg.solve(U, y)
    return x

# Ejemplo de uso:
if __name__ == "__main__":
    A = np.array([[3, 6, -1], [-3, -1, 2], [1, 7, 4]], dtype=float)
    b = np.array([2, 10, 3], dtype=float)
    resultado = descomposicion_lu(A, b)
    print("Resultado usando descomposición LU:", resultado)
