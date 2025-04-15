def resolver_sistema(metodo: str, *args, **kwargs):
    """
    Resuelve un sistema de ecuaciones usando el método especificado.

    Parámetros:
    - metodo: str -> Nombre del método ('gauss', 'gauss_jordan', 'cramer', 'jacobi', 'gauss_seidel', 'lu', 'biseccion')
    - args y kwargs: Argumentos necesarios para cada método.

    Retorna:
    - Solución del sistema.
    """

    if metodo == 'Gauss':
        from .Gauss import metodo_gauss
        return metodo_gauss(*args, **kwargs)

    elif metodo == 'Gauss_Jordan':
        from .Gauss_Jordan import metodo_gauss_jordan
        return metodo_gauss_jordan(*args, **kwargs)

    elif metodo == 'Cramer':
        from .Cramer import metodo_cramer
        return metodo_cramer(*args, **kwargs)

    elif metodo == 'Jacobi':
        from .Jacobi import metodo_jacobi
        return metodo_jacobi(*args, **kwargs)

    elif metodo == 'Gauss_Seidel':
        from .Gauss_Seidel import metodo_gauss_seidel
        return metodo_gauss_seidel(*args, **kwargs)

    elif metodo == 'LU':
        from .Descomposicion_LU import metodo_lu
        return metodo_lu(*args, **kwargs)

    elif metodo == 'Biseccion':
        from .Biseccion import metodo_biseccion
        return metodo_biseccion(*args, **kwargs)

    else:
        raise ValueError(f'Método {metodo} no reconocido')
