import math
from unittest import TestCase

class TestSqrt(TestCase):
    def test_sqrt(self, x, epsilon):
        expected = math.sqrt(x)
        actual = sqrt(x, epsilon)
        self.assertAlmostEqual(expected, actual, delta=epsilon / 10)

def sqrt(x, epsilon):
    approx = x / 2
    while abs(x - approx ** 2) > epsilon:
        approx = 0.5 * (approx + x / approx)
    return approx

if __name__ == '__main__':
    unittest.main()