import unittest


class TestLIS(unittest.TestCase):
    def test_lis(self):
        self.assertEqual(lis([10, 9, 2, 5, 3, 7, 101, 18]), 4)
        self.assertEqual(lis([4, 10, 4, 3, 2, 1]), 3)
        self.assertEqual(lis([1, 3, 6, 7, 9, 4, 10, 12]), 6)
        self.assertEqual(lis([5, 8, 12, 1, 3, 4, 7, 9]), 4)
        self.assertEqual(lis([]), 0)


if __name__ == "__main__":
    unittest.main()
