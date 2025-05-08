import unittest


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


class Testgcd(unittest.TestCase):
    def test_gcd(self):
        # Test case 1: Both positive integers
        self.assertEqual(gcd(4, 6), 2)
        # Test case 2: One zero
        self.assertEqual(gcd(0, 5), 5)
        # Test case 3: Negative numbers (gcd is always non-negative)
        self.assertEqual(gcd(-12, -18), 6)  # Since gcd is absolute value


if __name__ == "__main__":
    unittest.main()
