import unittest


class TestMaxSublistSum(unittest.TestCase):
    def test_empty_array(self):
        self.assertEqual(max_sublist_sum([]), 0)

    def test_positive_numbers(self):
        self.assertEqual(max_sublist_sum([1, 2, 3, 4]), 10)

    def test_negative_numbers(self):
        self.assertEqual(max_sublist_sum([-1, -2, -3, -4]), -1)

    def test_mixed_numbers(self):
        self.assertEqual(max_sublist_sum([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6)

    def test_all_negative_except_one(self):
        self.assertEqual(max_sublist_sum([-2, -3, 4, -1, -2, 1, 5, -3]), 7)

    def test_single_element(self):
        self.assertEqual(max_sublist_sum([5]), 5)

    def test_single_negative_element(self):
        self.assertEqual(max_sublist_sum([-5]), -5)

    def test_large_numbers(self):
        self.assertEqual(max_sublist_sum([1000, -500, 200, -300, 50]), 100)


if __name__ == "__main__":
    unittest.main()
