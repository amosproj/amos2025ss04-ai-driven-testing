import unittest

def get_factors(n):
    if n == 1:
        return []
    
    factors = []
    i = 2
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 1
    
    if n > 1:
        factors.append(n)
    
    return factors

# Test class for the get_factors function
class TestGetFactors(unittest.TestCase):
    def test_get_factors(self):
        self.assertEqual(get_factors(0), [])
        self.assertEqual(get_factors(1), [])
        self.assertEqual(get_factors(7), [7])
        self.assertEqual(get_factors(896), [2, 2, 2, 2, 2, 3, 7])

    def test_get_factors_inefficient(self):
        self.assertEqual(get_factors(0), [])
        self.assertEqual(get_factors(1), [])
        self.assertEqual(get_factors(7), [7])
        self.assertEqual(get_factors(896), [2, 2, 2, 2, 2, 3, 7])

if __name__ == '__main__':
    unittest.main()