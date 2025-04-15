import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from SC19013UNO.lineales import SolucionadorLineales

class TestLinealSolver(unittest.TestCase):
    def setUp(self):
        self.A = [
            [10, 2, 1],
            [2, 20, -2],
            [-2, 3, 10]
        ]

        self.b = [9, -44, 22]
        self.solucion_esperada = [1.0, -2.0, 3.0]
        self.tol = 1e-6

    def test_gauss(self):
        sol = SolucionadorLineales.gauss(self.A, self.b)
        for i in range(len(sol)):
            self.assertAlmostEqual(sol[i], self.solucion_esperada[i], delta=self.tol)

    def test_gauss_jordan(self):
        sol = SolucionadorLineales.gauss_jordan(self.A, self.b)
        for i in range(len(sol)):
            self.assertAlmostEqual(sol[i], self.solucion_esperada[i], delta=self.tol)

    def test_lu(self):
        sol = SolucionadorLineales.lu(self.A, self.b)
        for i in range(len(sol)):
            self.assertAlmostEqual(sol[i], self.solucion_esperada[i], delta=self.tol)

    def test_jacobi(self):
        sol = SolucionadorLineales.jacobi(self.A, self.b, max_iter=1000)
        for i in range(len(sol)):
            self.assertAlmostEqual(sol[i], self.solucion_esperada[i], delta=1e-2)  # Jacobi puede ser menos preciso

    def test_gauss_seidel(self):
        sol = SolucionadorLineales.gauss_seidel(self.A, self.b, max_iter=1000)
        for i in range(len(sol)):
            self.assertAlmostEqual(sol[i], self.solucion_esperada[i], delta=1e-3)

    def test_cramer(self):
        sol = SolucionadorLineales.cramer(self.A, self.b)
        for i in range(len(sol)):
            self.assertAlmostEqual(sol[i], self.solucion_esperada[i], delta=self.tol)

    def test_sistema_singular(self):
        A_singular = [
            [1, 1, 1],
            [1, 1, 1],  # Filas linealmente dependientes
            [1, 1, 1]
        ]
        with self.assertRaises(ValueError):
            SolucionadorLineales.gauss(A_singular, [1, 1, 1])

if __name__ == '__main__':
    unittest.main()