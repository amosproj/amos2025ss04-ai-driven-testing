import unittest


def bitcount(n):
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


class TestBitCount(unittest.TestCase):
    def test_bitcount_zero(self):
        self.assertEqual(bitcount(0), 0)

    def test_bitcount_one(self):
        self.assertEqual(bitcount(1), 1)

    def test_bitcount_two(self):
        self.assertEqual(bitcount(2), 1)

    def test_bitcount_three(self):
        self.assertEqual(bitcount(3), 2)

    def test_bitcount_four(self):
        self.assertEqual(bitcount(4), 1)

    def test_bitcount_eight(self):
        self.assertEqual(bitcount(8), 1)

    def test_bitcount_seven(self):
        self.assertEqual(bitcount(7), 3)


if __name__ == "__main__":
    unittest.main()
