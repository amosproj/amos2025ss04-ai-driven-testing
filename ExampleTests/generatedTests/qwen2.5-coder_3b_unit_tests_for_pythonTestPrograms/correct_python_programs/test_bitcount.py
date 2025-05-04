import unittest

class TestBitcount(unittest.TestCase):
    def test_bitcount(self):
        self.assertEqual(bitcount(0), 0)
        self.assertEqual(bitcount(1), 1)
        self.assertEqual(bitcount(2), 1)
        self.assertEqual(bitcount(3), 2)
        self.assertEqual(bitcount(4), 1)
        self.assertEqual(bitcount(5), 2)
        self.assertEqual(bitcount(6), 2)
        self.assertEqual(bitcount(7), 3)
        self.assertEqual(bitcount(8), 1)
        self.assertEqual(bitcount(9), 2)
        self.assertEqual(bitcount(10), 2)
        self.assertEqual(bitcount(11), 2)
        self.assertEqual(bitcount(12), 2)
        self.assertEqual(bitcount(13), 3)

if __name__ == '__main__':
    unittest.main()