def sqrt(x, epsilon):
    approx = x / 2
    while abs(x - approx * approx) > epsilon:
        approx = 0.5 * (approx + x / approx)
    return approx

import unittest


class TestSqrtFunction(unittest.TestCase):

    def test_sqrt(self):
        self.assertAlmostEqual(sqrt(4, 0.01), 2.0, delta=0.01)
        self.assertAlmostEqual(sqrt(9, 0.001), 3.0, delta=0.001)
        self.assertAlmostEqual(sqrt(2, 0.01), 1.4142, delta=0.01)
        self.assertAlmostEqual(sqrt(25, 0.001), 5.0, delta=0.001)

    def test_zero_input(self):
        with self.assertRaises(ValueError):
            sqrt(0, 0.01)

    def test_negative_input(self):
        with self.assertRaises(ValueError):
            sqrt(-1, 0.01)


if __name__ == '__main__':
    unittest.main()