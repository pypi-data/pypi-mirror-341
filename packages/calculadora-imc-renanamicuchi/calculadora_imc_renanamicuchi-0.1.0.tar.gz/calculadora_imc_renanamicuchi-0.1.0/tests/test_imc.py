import unittest
from calculadora_imc import calcular_imc, classificar_imc

class TestCalculadoraIMC(unittest.TestCase):
    def test_calcular_imc(self):
        self.assertAlmostEqual(calcular_imc(70, 1.75), 22.857, places=3)
    
    def test_classificar_imc(self):
        self.assertEqual(classificar_imc(22.86), "Peso normal")
        self.assertEqual(classificar_imc(17), "Abaixo do peso")
        self.assertEqual(classificar_imc(27), "Sobrepeso")
        self.assertEqual(classificar_imc(32), "Obesidade grau I")
        self.assertEqual(classificar_imc(37), "Obesidade grau II")
        self.assertEqual(classificar_imc(42), "Obesidade grau III")

if __name__ == '__main__':
    unittest.main()