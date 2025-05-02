import unittest

def get_factors(n):
    if n == 1:
        return []

    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return [i] + get_factors(n // i)

    return [n]

class TestGetFactors(unittest.TestCase):

    def test_get_factors_of_1(self):
        self.assertEqual(get_factors(1), [])

    def test_get_factors_of_even_number(self):
        result = get_factors(20)
        expected_result = [2, 10]
        self.assertCountEqual(result, expected_result)

    def test_get_factors_of_prime_number(self):
        result = get_factors(13)
        expected_result = [13] # As the function should not find any factors other than itself
        self.assertEqual(result, expected_result)

    def test_get_factors_of_large_composite_number(self):
        result = get_factors(100)
        expected_result = [2, 5, 10]
        self.assertCountEqual(sorted(result), sorted(expected_result))

if __name__ == '__main__':
    unittest.main()