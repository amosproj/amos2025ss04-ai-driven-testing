def bitcount(n):
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


class TestBitcount(unittest.TestCase):

    def test_bitcount_zero(self, n=0):
        self.assertEqual(bitcount(n), 0)

    def test_bitcount_positive(self, n=5):
        self.assertEqual(bitcount(n), bin(n).count('1'))

    def test_bitcount_negative(self, n=-3):
        self.assertEqual(bitcount(n), bitcount(abs(n)))

    def test_bitcount_all_set(self, n=0xFFFFFFFF):
        self.assertEqual(bitcount(n), 4)


if __name__ == '__main__':
    unittest.main()