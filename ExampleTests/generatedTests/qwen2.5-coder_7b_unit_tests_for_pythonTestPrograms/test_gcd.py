import unittest


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


class TestGCD(unittest.TestCase):
    def test_gcd_with_positive_numbers(self):
        self.assertEqual(gcd(48, 18), 6)

    def test_gcd_with_negative_numbers(self):
        self.assertEqual(gcd(-48, -18), 6)

    def test_gcd_with_one_zero(self):
        self.assertEqual(gcd(0, 5), 5)

    def test_gcd_with_both_zeroes(self):
        with self.assertRaises(ZeroDivisionError):
            gcd(0, 0)


if __name__ == "__main__":
    unittest.main()
