def bucketsort(arr, k):
    counts = [0] * k
    for x in arr:
        counts[x] += 1

    sorted_arr = []
    for i, count in enumerate(counts):
        sorted_arr.extend([i] * count)

    return sorted_arr


import unittest
from typing import List


class BucketSortTest(unittest.TestCase):
    def test_bucketsort(self) -> None:
        self.assertEqual(bucketsort([], 0), [])
        self.assertEqual(
            bucketsort([3, 1, 2, 2, 4, 5, 5, 5], 5), [1, 2, 2, 3, 4, 5, 5, 5]
        )

    def test_empty_array(self) -> None:
        self.assertEqual(bucketsort([], 0), [])

    def test_all_elements_same(self) -> None:
        self.assertEqual(bucketsort([3, 3, 3], 3), [3, 3, 3])

    def test_with_zeros(self) -> None:
        self.assertEqual(bucketsort([0, 1, 2, 0, 1, 2], 3), [0, 0, 1, 1, 2, 2])


if __name__ == "__main__":
    unittest.main()
