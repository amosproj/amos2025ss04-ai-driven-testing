import unittest

def get_factors(n):
    if n == 1:
        return []

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return [i] + get_factors(n // i)

    return [n]

class TestGetFactors(unittest.TestCase):

    def test_get_factors_1(self):
        self.assertEqual(get_factors(1), [])

    def test_get_factors_2(self):
        self.assertEqual(get_factors(2), [2])

    def test_get_factors_6(self):
        self.assertEqual(get_factors(6), [2, 3])

    def test_get_factors_12(self):
        self.assertEqual(get_factors(12), [2, 2, 3])

    def test_get_factors_36(self):
        self.assertEqual(get_factors(36), [2, 2, 3, 3])

    def test_get_factors_7(self):
        self.assertEqual(get_factors(7), [7])

    def test_get_factors_10(self):
        self.assertEqual(get_factors(10), [2, 5])

    def test_get_factors_28(self):
        self.assertEqual(get_factors(28), [2, 2, 7])


if __name__ == '__main__':
    unittest.main()