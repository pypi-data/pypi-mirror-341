# 7. Método de Bisección (para una ecuación no lineal)
def biseccion(f, a, b, tol=1e-10, max_iter=1000):
    if f(a) * f(b) >= 0:
        raise ValueError("La función debe tener signos opuestos en los extremos del intervalo")
    
    for _ in range(max_iter):
        c = (a + b) / 2
        if f(c) == 0 or (b - a) / 2 < tol:
            return c
        if f(c) * f(a) < 0:
            b = c
        else:
            a = c
    return (a + b) / 2


#prueba: 
if __name__ == "__main__":
    # Definimos una función ejemplo: f(x) = x^2 - 4
    def f(x):
        return x**2 - 4

    # Buscamos la raíz en el intervalo [1, 3]
    raiz = biseccion(f, 1, 3)
    print(f"La raíz encontrada es: {raiz}")