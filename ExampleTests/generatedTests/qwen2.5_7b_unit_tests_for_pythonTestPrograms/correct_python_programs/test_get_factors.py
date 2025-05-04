def get_factors(n):
    if n == 1:
        return []

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return [i] + get_factors(n // i)

    return [n]


import unittest

class TestGetFactors(unittest.TestCase):

    def test_get_factors(self):
        self.assertEqual(get_factors(1), [])
        self.assertEqual(get_factors(6), [2, 3])
        self.assertEqual(get_factors(10), [2, 5])
        self.assertEqual(get_factors(12), [2, 2, 3])
        self.assertEqual(get_factors(37), [37])

    def test_get_factors_with_large_number(self):
        self.assertEqual(get_factors(864), [2, 2, 2, 2, 2, 3, 3, 3])


if __name__ == '__main__':
    unittest.main()