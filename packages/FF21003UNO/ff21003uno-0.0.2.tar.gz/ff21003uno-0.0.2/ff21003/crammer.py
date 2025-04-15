import numpy as np

def crammer(A, b):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Crammer.
    
    Parámetros:
    A (numpy.ndarray): Matriz de coeficientes.
    b (numpy.ndarray): Vector de constantes.
    
    """
    det_A = np.linalg.det(A)
    if det_A == 0:
        raise ValueError("El determinante de A es cero, el sistema no tiene solución única.")

    n = len(A)
    x = np.zeros(n)
    for i in range(n):
        A_copy = A.copy()
        A_copy[:, i] = b
        x[i] = np.linalg.det(A_copy) / det_A
    return x

# Ejemplo de uso:
if __name__ == "__main__":
    A = np.array([[-2, 4, -1], [4, -1, 7], [3, 4, 2]], dtype=float)
    b = np.array([3, 12, 5], dtype=float)
    resultado = crammer(A, b)
    print("Resultado usando el método de Crammer:", resultado)
