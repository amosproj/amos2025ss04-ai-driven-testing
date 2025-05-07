def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


import unittest


class TestGCD(unittest.TestCase):
    def test_gcd_positive_numbers(self):
        self.assertEqual(gcd(12, 18), 6)
        self.assertEqual(gcd(48, 18), 6)
        self.assertEqual(gcd(12, 6), 6)

    def test_gcd_one_number_is_zero(self):
        self.assertEqual(gcd(12, 0), 12)
        self.assertEqual(gcd(0, 18), 18)
        self.assertEqual(gcd(0, 0), 0)

    def test_gcd_same_numbers(self):
        self.assertEqual(gcd(5, 5), 5)
        self.assertEqual(gcd(10, 10), 10)

    def test_gcd_relatively_prime_numbers(self):
        self.assertEqual(gcd(7, 11), 1)
        self.assertEqual(gcd(13, 17), 1)


if __name__ == "__main__":
    unittest.main()
