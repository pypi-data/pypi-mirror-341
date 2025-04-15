import numpy as np

def gauss_jordan(A, b):
    n = len(A)
    matriz_aum = np.hstack([A, b.reshape(-1, 1)])

    # Eliminación hacia adelante
    for i in range(n):
        matriz_aum[i, :] /= matriz_aum[i, i]
        for j in range(n):
            if i != j:
                matriz_aum[j, :] -= matriz_aum[i, :] * matriz_aum[j, i]

    return matriz_aum[:, -1]
