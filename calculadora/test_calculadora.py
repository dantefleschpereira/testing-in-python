import unittest
from calculadora import soma


class TestCalculadora(unittest.TestCase):
    def test_soma_5_e_5_deve_retornar_10(self):
        self.assertEqual(soma(5, 5), 10)

    def test_2_negativo_e_6_deve_retornar_4(self):
        self.assertEqual(soma(-2, 6), 4)


unittest.main(verbosity=2)
