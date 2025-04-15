class EcuacionesNoLineales:
    def biseccion(self, f, a, b, tol=1e-10, max_iter=100):
        """
        Resuelve una ecuación no lineal haciendo uso del método de Bisección.

        Parámetros:
        f -> Función que representa la ecuación.
        a -> Limite inferior del intervalo.
        b -> Limite superior del intervalo.
        tol -> Tolerancia para el criterio de parada.
        max_iter -> Número máximo de iteraciones.

        Retorno:
        c -> Raiz aproximada de la ecuacion.
        """

        if f(a) * f(b) > 0:
            raise ValueError("La función debe cambiar de signo en el itervalo [a, b].")
        
        for _ in range(max_iter):
            c = (a + b)/2.0

            if abs(f(c))<tol:
                return c
            
            #Si f(c) tiene el mismo signo que f(a), entonces la raíz está en [c, b]
            elif f(a) * f(c) < 0:
                b = c
            else:
                a = c
        raise ValueError("El método no convergió en el número máximo de iteraciones.")
