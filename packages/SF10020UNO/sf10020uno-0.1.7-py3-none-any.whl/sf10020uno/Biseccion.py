from fractions import Fraction

def bisection_method(f, a, b, tolerance, max_iter):
    if f(a) * f(b) >= 0:
        print("El método de bisección no garantiza una raíz en el intervalo dado.")
        return None

    print("Iteraciones Método de Bisección:\n")

    for k in range(1, max_iter + 1):
        c = (a + b) / 2
        print(f"Iteración {k}: a={a}, b={b}, c={c}, f(c)={f(c)}")

        if abs(f(c)) < tolerance or (b - a) / 2 < tolerance:
            print(f"\nConvergencia alcanzada en la iteración {k}")
            break

        if f(a) * f(c) < 0:
            b = c
        else:
            a = c

    else:
        print("\nSe alcanzó el número máximo de iteraciones sin convergencia.")

    print(f"\nRaíz encontrada: x = {Fraction(c).limit_denominator()}")
    print(f"Valor de f(x) en la raíz encontrada: {f(c)}")
    return c


# Esta función será utilizada por la librería
def metodo_biseccion(funcion_str, intervalo, tolerancia, max_iter):
    # Convertir string a función usando eval
    def f(x):
        return eval(funcion_str)

    a, b = intervalo
    return bisection_method(f, a, b, tolerancia, max_iter)
