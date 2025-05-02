import unittest

def sqrt(x, epsilon):
    approx = x / 2
    while abs(x - approx ** 2) > epsilon:
        approx = 0.5 * (approx + x / approx)
    return approx

class TestSqrt(unittest.TestCase):
    def test_sqrt_small_epsilon(self):
        result = sqrt(4, 0.1)
        self.assertAlmostEqual(result, 2.0, places=1)

    def test_sqrt_large_epsilon(self):
        result = sqrt(9, 1)
        self.assertEqual(result, 3)

    def test_sqrt_zero_epsilon(self):
        result = sqrt(25, 0)
        self.assertEqual(result, 5)

if __name__ == '__main__':
    unittest.main()