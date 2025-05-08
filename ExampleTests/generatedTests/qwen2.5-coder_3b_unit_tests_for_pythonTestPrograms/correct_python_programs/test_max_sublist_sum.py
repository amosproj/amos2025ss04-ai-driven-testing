import unittest


class TestMaxSublistSum(unittest.TestCase):
    def test_max_sublist_sum(self):
        self.assertEqual(max_sublist_sum([1, 2, -4, 6, 3]), 9)
        self.assertEqual(max_sublist_sum([-1, -2, -3]), -1)
        self.assertEqual(max_sublist_sum([0, -1, -2, 0]), 0)
        self.assertEqual(max_sublist_sum([-1, 3, -4, 5, 6]), 11)
        self.assertEqual(max_sublist_sum([]), 0)


if __name__ == "__main__":
    unittest.main()
