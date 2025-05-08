def bitcount(n):
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


import unittest


class TestBitCount(unittest.TestCase):
    def test_zero(self):
        self.assertEqual(bitcount(0), 0)

    def test_one(self):
        self.assertEqual(bitcount(1), 1)

    def test_two(self):
        self.assertEqual(bitcount(2), 1)

    def test_eight(self):
        self.assertEqual(bitcount(8), 1)

    def test_nine(self):
        self.assertEqual(bitcount(9), 2)

    def test_sixteen(self):
        self.assertEqual(bitcount(16), 1)

    def test_thirty_two(self):
        self.assertEqual(bitcount(32), 1)

    def test_negative_one(self):
        self.assertEqual(bitcount(-1), 32)

    def test_large_number(self):
        self.assertEqual(bitcount(255), 8)

    def test_another_large_number(self):
        self.assertEqual(bitcount(1023), 10)


if __name__ == "__main__":
    unittest.main()
