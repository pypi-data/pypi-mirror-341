import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from SC19013UNO.no_lineales import SolucionadorNoLineales
import math

class TestNonLinearSolver(unittest.TestCase):
    def test_biseccion(self):
        # Test para √2
        f = lambda x: x**2 - 2
        sol = SolucionadorNoLineales.biseccion(f, 1, 2)
        self.assertAlmostEqual(sol, math.sqrt(2), delta=1e-6)

        # Test para cos(x) = 0 en [0, 2]
        sol_cos = SolucionadorNoLineales.biseccion(math.cos, 0, 2)
        self.assertAlmostEqual(sol_cos, math.pi/2, delta=1e-6)

    def test_biseccion_error(self):
        # Test para intervalo sin cambio de signo
        f = lambda x: x**2
        with self.assertRaises(ValueError):
            SolucionadorNoLineales.biseccion(f, 1, 2)

    def test_biseccion_max_iter(self):
        # Test con tolerancia muy exigente
        f = lambda x: x**3 - x - 2
        sol = SolucionadorNoLineales.biseccion(f, 1, 2, tol=1e-12, max_iter=5)
        self.assertTrue(1 <= sol <= 2)  # Al menos debería devolver un valor en el intervalo

if __name__ == '__main__':
    unittest.main()