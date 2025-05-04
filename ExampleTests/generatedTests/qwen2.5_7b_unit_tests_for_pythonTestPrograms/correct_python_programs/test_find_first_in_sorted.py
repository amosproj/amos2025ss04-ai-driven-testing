def find_first_in_sorted(arr, x):
    lo = 0
    hi = len(arr)

    while lo + 1 <= hi:
        mid = (lo + hi) // 2

        if x == arr[mid] and (mid == 0 or x != arr[mid - 1]):
            return mid

        elif x <= arr[mid]:
            hi = mid

        else:
            lo = mid + 1

    return -1


import unittest
from typing import List

class TestFindFirstInSorted(unittest.TestCase):
    def test_find_first_in_sorted(self) -> None:
        self.assertEqual(find_first_in_sorted([1, 2, 3, 4, 5], 3), 2)
        self.assertEqual(find_first_in_sorted([1, 2, 2, 2, 3, 4, 5], 2), 1)
        self.assertEqual(find_first_in_sorted([1, 2, 3, 4, 5], 6), -1)
        self.assertEqual(find_first_in_sorted([], 1), -1)
        self.assertEqual(find_first_in_sorted([1], 1), 0)
        self.assertEqual(find_first_in_sorted([1, 3, 5], 2), -1)

if __name__ == '__main__':
    unittest.main()