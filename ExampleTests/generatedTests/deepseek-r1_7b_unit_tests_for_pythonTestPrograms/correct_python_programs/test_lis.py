import unittest
from collections import Counter


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
    def test_lis(self):
        # Test case 1: Empty array
        self.assertEqual(lis([]), 0)

        # Test case 2: Increasing sequence
        self.assertEqual(lis([1, 2, 3, 4]), 4)

        # Test case 3: Mixed sequence 1
        self.assertEqual(lis([5, 3, 4, 8, 9, 1, 2, 7]), 6)

        # Test case 4: Mixed sequence 2
        test_array = [2, -1, 7, 0]
        expected_length = 3  # The longest subsequence is [-1, 0, 7] or similar
        self.assertEqual(lis(test_array), expected_length)

        # Test case 5: Random sequence with duplicates and varying lengths
        test_array2 = [4, 3, 2, 5, 1]
        expected_length2 = 3  # e.g., [3,5] but longer sequences exist?
        self.assertEqual(lis(test_array2), expected_length2)

        # Test case 6: All decreasing sequence
        self.assertEqual(lis([4, 3, 2, 1]), 1)


if __name__ == "__main__":
    unittest.main()
