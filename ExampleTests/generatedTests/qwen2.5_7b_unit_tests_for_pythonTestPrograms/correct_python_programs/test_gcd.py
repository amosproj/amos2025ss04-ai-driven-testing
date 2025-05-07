def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


import unittest


class TestGCD(unittest.TestCase):
    def test_gcd(self):
        self.assertEqual(gcd(48, 18), 6)
        self.assertEqual(gcd(1071, 462), 21)
        self.assertEqual(gcd(35, 0), 35)
        self.assertEqual(gcd(0, 10), 10)
        self.assertEqual(gcd(1, 1), 1)
        self.assertEqual(gcd(0, 0), 0)


if __name__ == "__main__":
    unittest.main()
