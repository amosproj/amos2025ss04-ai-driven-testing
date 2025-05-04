def lis(arr):
    ends = {}
    longest = 0

    for i, val in enumerate(arr):

        prefix_lengths = [j for j in range(1, longest + 1) if arr[ends[j]] < val]

        length = max(prefix_lengths) if prefix_lengths else 0

        if length == longest or val < arr[ends[length + 1]]:
            ends[length + 1] = i
            longest = max(length + 1, longest)

    return longest


import unittest
from collections.abc import Callable

class TestLIS(unittest.TestCase):
    def test_lis(self) -> None:
        self.assertEqual(lis([10, 9, 2, 5, 3, 7, 101, 18]), 4)
        self.assertEqual(lis([0, 8, 4, 12, 2, 10, 6, 14, 1, 9, 5, 13, 3, 11, 7, 15]), 6)
        self.assertEqual(lis([]), 0)
        self.assertEqual(lis([1]), 1)
        self.assertEqual(lis([1, 2]), 2)
        self.assertEqual(lis([2, 1]), 1)


if __name__ == '__main__':
    unittest.main()