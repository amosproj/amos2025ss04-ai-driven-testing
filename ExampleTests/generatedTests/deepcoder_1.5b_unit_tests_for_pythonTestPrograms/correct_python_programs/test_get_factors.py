import unittest


def get_factors(n):
    if n == 1:
        return []
    
    factors = []
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            factors.append(i)
            remaining = n // i
            temp_factors = get_factors(remaining)
            for f in temp_factors:
                factors.append(f)
    
    factors.append(n)
    return factors

class TestgetFactors(unittest.TestCase):
    def test_get_factors(self, n):
        if n == 1:
            self.assertEqual([], "n=1 should return empty list")
        else:
            result = get_factors(n)
            expected = [i for i in range(2, int(n ** 0.5) + 1) if (n // i == 1 and i != n) or (n % i == 0 and i < n) or n % i == 0]
            self.assertEqual(result, expected)

def test_get_factors_2(self, n):
    result = get_factors(n)
    expected = [i for i in range(2, int(n ** 0.5) + 1) if (n // i == 1 and i != n) or (n % i == 0 and i < n) or n % i == 0]
    self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()