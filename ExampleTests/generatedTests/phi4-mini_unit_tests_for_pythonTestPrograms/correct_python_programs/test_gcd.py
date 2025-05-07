import unittest


def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


class TestGCD(unittest.TestCase):
    def test_gcd_positive_integers(self):
        self.assertEqual(gcd(48, 18), 6)

    def test_gcd_zero(self):
        with self.subTest(a=10, b=0):
            self.assertEqual(gcd(10, 0), 10)

    def test_gcd_negative_numbers(self):
        with self.subTest(a=-48, b=-18):
            self.assertEqual(gcd(-48, -18), abs(gcd(48, 18)))


if __name__ == "__main__":
    unittest.main()
