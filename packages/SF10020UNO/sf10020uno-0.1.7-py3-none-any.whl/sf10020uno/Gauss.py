import numpy as np
from fractions import Fraction

# Función para implementar la eliminación de Gauss manualmente
def gauss_elimination(A, b):
    n = len(b)
    # Crear una matriz aumentada [A|b]
    augmented = np.column_stack((A, b))
    
    # Imprimir la matriz aumentada inicial
    print("Matriz aumentada inicial:")
    print(augmented)
    print()
    
    # Eliminación hacia adelante
    for i in range(n):
        # Pivoteo parcial: buscar el elemento máximo en la columna
        max_row = i + np.argmax(abs(augmented[i:, i]))
        if max_row != i:
            augmented[[i, max_row]] = augmented[[max_row, i]]
            print(f"Intercambio de filas {i+1} y {max_row+1}:")
            print(augmented)
            print()
        
        # Escalar el pivote a 1
        pivot = augmented[i, i]
        augmented[i] = augmented[i] / pivot
        print(f"Fila {i+1} dividida por {pivot}:")
        print(augmented)
        print()
        
        # Eliminar los elementos debajo del pivote
        for j in range(i + 1, n):
            factor = augmented[j, i]
            augmented[j] = augmented[j] - factor * augmented[i]
            print(f"Fila {j+1} = Fila {j+1} - {factor} * Fila {i+1}:")
            print(augmented)
            print()
    
    # Sustitución hacia atrás
    x = np.zeros(n)
    for i in range(n-1, -1, -1):
        x[i] = augmented[i, -1]
        for j in range(i+1, n):
            x[i] -= augmented[i, j] * x[j]
    
    # Convertir a fracciones para presentación
    solution_fractions = [Fraction(float(val)).limit_denominator() for val in x]

    print("Solución encontrada:")
    for idx, val in enumerate(solution_fractions, start=1):
        print(f"x{idx} = {val}")

    # Verificación de la solución
    print("\nVerificación:")
    for i, row in enumerate(A):
        result = np.dot(row, x)
        print(f"Ecuación {i+1}: {result} = {b[i]} {'✓' if abs(result - b[i]) < 1e-10 else '✗'}")

    # Solución definitiva usando NumPy para comparación
    numpy_solution = np.linalg.solve(A, b)
    print("\nSolución Definitiva:")
    for idx, val in enumerate(numpy_solution, start=1):
        print(f"x{idx} = {Fraction(val).limit_denominator()}")

    return x

# Esta función será utilizada por la librería
def metodo_gauss(A, b):
    return gauss_elimination(np.array(A, dtype=float), np.array(b, dtype=float))