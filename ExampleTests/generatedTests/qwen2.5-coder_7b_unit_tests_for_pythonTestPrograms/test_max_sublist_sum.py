import unittest


def max_sublist_sum(arr):
    max_ending_here = 0
    max_so_far = 0

    for x in arr:
        max_ending_here = max(0, max_ending_here + x)
        max_so_far = max(max_so_far, max_ending_here)

    return max_so_far


class TestMaxSublistSum(unittest.TestCase):
    def test_empty_array(self):
        self.assertEqual(max_sublist_sum([]), 0)

    def test_single_element_positive(self):
        self.assertEqual(max_sublist_sum([1]), 1)

    def test_single_element_negative(self):
        self.assertEqual(max_sublist_sum([-1]), 0)

    def test_multiple_elements_with_positive_sum(self):
        self.assertEqual(max_sublist_sum([3, -2, 5, -1]), 8)

    def test_multiple_elements_with_all_negatives(self):
        self.assertEqual(max_sublist_sum([-1, -2, -3, -4]), 0)

    def test_multiple_elements_with_mixed_values(self):
        self.assertEqual(max_sublist_sum([3, -2, 5, -1, -4, 6]), 9)

    def test_array_with_zero(self):
        self.assertEqual(max_sublist_sum([0, -2, 5, -1]), 5)


if __name__ == "__main__":
    unittest.main()
