def bitcount(n):
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count


import unittest


class TestBitCount(unittest.TestCase):
    def test_bitcount(self):
        # Test case 1: n = 0 (should return 0)
        self.assertEqual(bitcount(0), 0)

        # Test case 2: n = 1 (binary '1', should return 1)
        self.assertEqual(bitcount(1), 1)

        # Test case 3: n = 2 (binary '10', should return 1)
        self.assertEqual(bitcount(2), 1)

        # Test case 4: n = 3 (binary '11', should return 2)
        self.assertEqual(bitcount(3), 2)

        # Test case 5: n = 5 (binary '101', should return 2)
        self.assertEqual(bitcount(5), 2)

        # Test case 6: n = 768 (binary '1100000000', should return 1)
        self.assertEqual(bitcount(768), 1)


if __name__ == "__main__":
    unittest.main()
