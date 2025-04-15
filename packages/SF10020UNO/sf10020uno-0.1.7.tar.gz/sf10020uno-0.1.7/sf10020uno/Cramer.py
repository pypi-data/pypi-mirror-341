import numpy as np
from fractions import Fraction

# Método de Cramer
def cramer_method(A, b):
    n = len(b)
    det_A = np.linalg.det(A)

    print(f"Determinante de A: {det_A}")
    if abs(det_A) < 1e-10:
        raise ValueError("El sistema no tiene solución única (determinante cero).")

    solutions = []

    for i in range(n):
        A_i = A.copy()
        A_i[:, i] = b
        det_Ai = np.linalg.det(A_i)
        print(f"Determinante de A reemplazando columna {i+1}: {det_Ai}")
        x_i = det_Ai / det_A
        solutions.append(x_i)

    # Convertir a fracciones
    solution_fractions = [Fraction(val).limit_denominator() for val in solutions]

    print("\nSolución encontrada:")
    for idx, val in enumerate(solution_fractions, start=1):
        print(f"x{idx} = {val}")

    print("\nVerificación:")
    for i, row in enumerate(A):
        result = np.dot(row, solutions)
        print(f"Ecuación {i+1}: {result} = {b[i]} {'✓' if abs(result - b[i]) < 1e-10 else '✗'}")

    # Comparar con numpy
    numpy_solution = np.linalg.solve(A, b)
    print("\nSolución Definitiva")
    for idx, val in enumerate(numpy_solution, start=1):
        print(f"x{idx} = {Fraction(val).limit_denominator()}")

    return solutions

# Esta función será utilizada por la librería
def metodo_cramer(A, b):
    return cramer_method(np.array(A, dtype=float), np.array(b, dtype=float))
