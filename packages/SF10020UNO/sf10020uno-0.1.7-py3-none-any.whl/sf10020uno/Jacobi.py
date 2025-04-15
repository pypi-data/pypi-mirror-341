import numpy as np
from fractions import Fraction

def jacobi_method(A, b, x0, max_iter, tolerance):
    n = len(b)
    x = x0.copy()

    print("Iteraciones del Método de Jacobi:\n")

    for k in range(max_iter):
        x_new = np.zeros(n)

        print(f"Iteración {k+1}:")
        for i in range(n):
            suma = sum(A[i][j] * x[j] for j in range(n) if j != i)
            x_new[i] = (b[i] - suma) / A[i][i]
            print(f"x{i+1} = {x_new[i]}")

        print()

        error = np.linalg.norm(x_new - x, ord=np.inf)

        if error < tolerance:
            print(f"Convergencia alcanzada en la iteración {k+1}")
            break

        x = x_new.copy()

    return x


# Esta función será utilizada por la librería
def metodo_jacobi(A, b, x0=None, max_iter=100, tolerance=1e-6):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)

    if x0 is None:
        x0 = np.zeros(len(b))

    # Ejecutar método
    solution = jacobi_method(A, b, x0, max_iter, tolerance)

    # Mostrar resultados como fracciones
    solution_fractions = [Fraction(float(val)).limit_denominator() for val in solution]

    print("Solución encontrada:")
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