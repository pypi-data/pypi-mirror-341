class SolucionadorNoLineales:
    """Clase que implementa métodos para resolver ecuaciones no lineales."""
    
    @staticmethod
    def biseccion(f, a, b, tol=1e-6, max_iter=100):
        """
        Método de bisección para encontrar raíces de f(x) = 0 en [a, b].
        
        Args:
            f: Función a evaluar
            a, b: Extremos del intervalo
            tol: Tolerancia para la solución
            max_iter: Máximo número de iteraciones
            
        Returns:
            float: Aproximación de la raíz
        Raises:
            ValueError: Si no hay cambio de signo en el intervalo
            RuntimeError: Si no converge en max_iter iteraciones
        """
        if f(a) * f(b) >= 0:
            raise ValueError("No hay cambio de signo en [a, b].")
        
        for _ in range(max_iter):
            c = (a + b) / 2
            if abs(f(c)) < tol:
                return c
            if f(a) * f(c) < 0:
                b = c
            else:
                a = c
        return (a + b) / 2