import numpy as np

def eliminacion_gauss():
    """
    Resuelve un sistema de ecuaciones lineales usando la eliminación de Gauss,
    solicitando al usuario ingresar los coeficientes y el vector de términos independientes.
    """
    n = int(input("Ingrese el número de ecuaciones (y variables): "))
    
    matriz = []
    print("Ingrese los coeficientes de la matriz (una fila por línea, separados por espacios):")
    for i in range(n):
        fila = list(map(float, input(f"Fila {i+1}: ").split()))
        matriz.append(fila)
    
    A = np.array(matriz, dtype=float)
    
    print("Ingrese el vector de términos independientes (separado por espacios):")
    b = np.array(list(map(float, input("Vector b: ").split())), dtype=float)
    
    aumentada = np.hstack([A, b.reshape(-1, 1)])

    for i in range(n):
        for j in range(i + 1, n):
            razon = aumentada[j, i] / aumentada[i, i]
            aumentada[j, i:] -= razon * aumentada[i, i:]

    # Sustitución hacia atrás
    solucion = np.zeros(n)
    for i in range(n - 1, -1, -1):
        solucion[i] = (aumentada[i, -1] - np.dot(aumentada[i, i+1:n], solucion[i+1:])) / aumentada[i, i]

    print("Resultado usando eliminación de Gauss:", solucion)
