import numpy as np

def jacobi(A, b, tol=1e-10, max=1000):
    """
    Resuelve un sistema de ecuaciones lineales usando el método de Jacobi.
    
    Parámetros:
    A (numpy.ndarray): Matriz de coeficientes.
    b (numpy.ndarray): Vector de constantes.
    tol (float): Tolerancia para la convergencia.
    max (int): Número máximo de iteraciones.
    
    """
    n = len(A)
    x = np.zeros_like(b)

    for _ in range(max):
        x_new = np.copy(x)
        for i in range(n):
            sum_Ax = np.dot(A[i, :], x) - A[i, i] * x[i]
            x_new[i] = (b[i] - sum_Ax) / A[i, i]
        if np.linalg.norm(x_new - x, ord=np.inf) < tol:
            break
        x = x_new
    return x

# Ejemplo de uso:
if __name__ == "__main__":
    A = np.array([[3, 8, -1], [-3, -1, 7], [6, 5, 2]], dtype=float)
    b = np.array([4, 5, 7], dtype=float)
    resultado = jacobi(A, b)
    print("Resultado usando el método de Jacobi:", resultado)
