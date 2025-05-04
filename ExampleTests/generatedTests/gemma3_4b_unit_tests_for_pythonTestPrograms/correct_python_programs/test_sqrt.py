import unittest

def sqrt(x, epsilon):
    approx = x / 2
    while abs(x - approx ** 2) > epsilon:
        approx = 0.5 * (approx + x / approx)
    return approx

class TestSqrt(unittest.TestCase):

    def test_sqrt_positive_number(self):
        self.assertAlmostEqual(sqrt(9, 0.001), 3.0, places=4)
        self.assertAlmostEqual(sqrt(2, 0.001), 1.4142, places=4)
        self.assertAlmostEqual(sqrt(16, 0.001), 4.0, places=4)

    def test_sqrt_zero(self):
        self.assertEqual(sqrt(0, 0.001), 0.0, places=4)

    def test_sqrt_one(self):
        self.assertEqual(sqrt(1, 0.001), 1.0, places=4)

    def test_sqrt_large_number(self):
        self.assertAlmostEqual(sqrt(10000, 0.001), 100.0, places=4)

    def test_sqrt_negative_number(self):
        with self.assertRaises(ValueError):
            sqrt(-1, 0.001)
            
    def test_sqrt_float(self):
        self.assertAlmostEqual(sqrt(2.0, 0.001), 1.4142, places=4)
        self.assertAlmostEqual(sqrt(2.25, 0.001), 1.5, places=4)


if __name__ == '__main__':
    unittest.main()