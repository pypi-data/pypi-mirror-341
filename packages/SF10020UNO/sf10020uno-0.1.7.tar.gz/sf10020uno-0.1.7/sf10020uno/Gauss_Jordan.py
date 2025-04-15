import numpy as np
from fractions import Fraction

# Método de Gauss-Jordan
def gauss_jordan_elimination(A, b):
    n = len(b)
    augmented = np.column_stack((A, b))

    print("Matriz aumentada inicial:")
    print(augmented)
    print()

    for i in range(n):
        # Pivoteo parcial
        max_row = i + np.argmax(abs(augmented[i:, i]))
        if max_row != i:
            augmented[[i, max_row]] = augmented[[max_row, i]]
            print(f"Intercambio de filas {i+1} y {max_row+1}:")
            print(augmented)
            print()

        # Escalar la fila para que el pivote sea 1
        pivot = augmented[i, i]
        augmented[i] = augmented[i] / pivot
        print(f"Fila {i+1} dividida por {pivot}:")
        print(augmented)
        print()

        # Hacer ceros en las demás filas
        for j in range(n):
            if j != i:
                factor = augmented[j, i]
                augmented[j] = augmented[j] - factor * augmented[i]
                print(f"Fila {j+1} = Fila {j+1} - {factor} * Fila {i+1}:")
                print(augmented)
                print()

    # Extraer la solución
    x = augmented[:, -1]

    # Convertir a fracciones para mostrar resultados exactos
    solution_fractions = [Fraction(float(val)).limit_denominator() for val in x]

    print("Solución encontrada:")
    for idx, val in enumerate(solution_fractions, start=1):
        print(f"x{idx} = {val}")

    print("\nVerificación:")
    for i, row in enumerate(A):
        result = np.dot(row, x)
        print(f"Ecuación {i+1}: {result} = {b[i]} {'✓' if abs(result - b[i]) < 1e-10 else '✗'}")

    # Comparación con NumPy
    numpy_solution = np.linalg.solve(A, b)
    print("\nSolución Definitiva:")
    for idx, val in enumerate(numpy_solution, start=1):
        print(f"x{idx} = {Fraction(val).limit_denominator()}")

    return x

# Esta función será utilizada por la librería
def metodo_gauss_jordan(A, b):
    return gauss_jordan_elimination(np.array(A, dtype=float), np.array(b, dtype=float))