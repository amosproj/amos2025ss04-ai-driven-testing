import unittest


def sqrt(x, epsilon):
    approx = x / 2
    while abs(x - approx * approx) > epsilon:
        approx = 0.5 * (approx + x / approx)
    return approx


class TestSqrt(unittest.TestCase):
    def test_sqrt_positive(self):
        self.assertAlmostEqual(sqrt(4, 1e-10), 2)

    def test_sqrt_zero(self):
        self.assertEqual(sqrt(0, 1e-10), 0)

    def test_sqrt_negative_float(self):
        with self.assertRaises(ValueError):
            sqrt(-4, 1e-10)

    def test_sqrt_edge_case_small_epsilon(self):
        epsilon = int(1 / (2 * abs(sqrt(25))))
        result = sqrt(25, epsilon)  # should converge quickly
        expected = math.sqrt(25)

        self.assertAlmostEqual(result, expected, delta=epsilon / 10)

    def test_sqrt_too_large_epsilon(self):
        x_value = 10000
        too_small_epsilon = int(x_value / (2 * abs(math.sqrt(x_value))))
        result = sqrt(
            x_value, too_small_epsilon
        )  # should converge slowly or not at all

        self.assertAlmostEqual(
            result, math.sqrt(x_value), delta=too_small_epsilon / 10
        )


if __name__ == "__main__":
    unittest.main()
