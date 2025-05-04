import unittest

class TestGCD(unittest.TestCase):
    def test_gcd(self):
        self.assertEqual(gcd(48, 18), 6)
        self.assertEqual(gcd(56, 98), 14)
        self.assertEqual(gcd(25, 15), 5)
        self.assertEqual(gcd(101, 103), 1)  # Test case with prime numbers
        self.assertEqual(gcd(0, 5), 5)       # Edge case where b is zero
        self.assertEqual(gcd(5, 0), 5)       # Edge case where a is zero

if __name__ == '__main__':
    unittest.main()