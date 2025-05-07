import unittest


def lis(arr):
    ends = {}
    longest = 0

    for i, val in enumerate(arr):
        prefix_lengths = [
            j for j in range(1, longest + 1) if arr[ends[j]] < val
        ]

        length = max(prefix_lengths) if prefix_lengths else 0

        if length == longest or val < arr[ends[length + 1]]:
            ends[length + 1] = i
            longest = max(length + 1, longest)

    return longest


class TestLIS(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(lis([]), 0)

    def test_single_element_list(self):
        self.assertEqual(lis([3]), 1)

    def test_two_elements_increasing_order_list(self):
        self.assertEqual(lis([2, 4]), 1)

    def test_two_elements_decreasing_order_list(self):
        self.assertEqual(lis([4, 2]), 0)

    def test_multiple_elements_with_largest_length_subsequence(self):
        self.assertEqual(lis([10, 9, 8, 7, 6, 5, 3, 1]), 4)

    def test_no_increasing_order_subsequences(self):
        self.assertEqual(lis([1, 2, 0, 5, 6, -1]), 0)


if __name__ == "__main__":
    unittest.main()
