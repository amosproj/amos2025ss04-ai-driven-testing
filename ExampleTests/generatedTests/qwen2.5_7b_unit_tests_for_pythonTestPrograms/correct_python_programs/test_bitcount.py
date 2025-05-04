def bitcount(n):
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


import unittest

class TestBitCount(unittest.TestCase):

    def test_bitcount(self):
        self.assertEqual(bitcount(0), 0)
        self.assertEqual(bitcount(1), 1)
        self.assertEqual(bitcount(2), 1)
        self.assertEqual(bitcount(3), 2)
        self.assertEqual(bitcount(4), 1)
        self.assertEqual(bitcount(7), 3)
        self.assertEqual(bitcount(8), 1)
        self.assertEqual(bitcount(9), 2)
        self.assertEqual(bitcount(10), 2)
        self.assertEqual(bitcount(15), 4)

if __name__ == '__main__':
    unittest.main()