import numpy as np
from fractions import Fraction

def lu_decomposition(A):
    n = len(A)
    L = np.zeros((n, n))
    U = np.zeros((n, n))

    # Descomposición LU
    for i in range(n):
        # Calcular U
        for j in range(i, n):
            suma = sum(L[i][k] * U[k][j] for k in range(i))
            U[i][j] = A[i][j] - suma

        # Calcular L
        L[i][i] = 1
        for j in range(i+1, n):
            suma = sum(L[j][k] * U[k][i] for k in range(i))
            L[j][i] = (A[j][i] - suma) / U[i][i]

    return L, U


def forward_substitution(L, b):
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        suma = sum(L[i][j] * y[j] for j in range(i))
        y[i] = (b[i] - suma)
    return y


def backward_substitution(U, y):
    n = len(y)
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        suma = sum(U[i][j] * x[j] for j in range(i+1, n))
        x[i] = (y[i] - suma) / U[i][i]
    return x


# Esta función será utilizada por la librería
def metodo_lu(A, b):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    # Ejecutar método LU
    L, U = lu_decomposition(A)

    print("Matriz L (Triangular Inferior):")
    print(L)
    print("\nMatriz U (Triangular Superior):")
    print(U)

    # Sustitución hacia adelante
    y = forward_substitution(L, b)

    # Sustitución hacia atrás
    solution = backward_substitution(U, y)

    # Mostrar solución como fracciones
    solution_fractions = [Fraction(float(val)).limit_denominator() for val in solution]

    print("\nSolución encontrada:")
    for idx, val in enumerate(solution_fractions, start=1):
        print(f"x{idx} = {val}")

    print("\nVerificación:")
    for i, row in enumerate(A):
        result = np.dot(row, solution)
        print(f"Ecuación {i+1}: {result} = {b[i]} {'✓' if abs(result - b[i]) < 1e-6 else '✗'}")

    # Comparar con numpy
    numpy_solution = np.linalg.solve(A, b)
    print("\nSolución Definitiva:")
    for idx, val in enumerate(numpy_solution, start=1):
        print(f"x{idx} = {Fraction(val).limit_denominator()}")

    return solution
