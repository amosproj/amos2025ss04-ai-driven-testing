import unittest


def find_first_in_sorted(arr, x):
    lo = 0
    hi = len(arr)

    while lo < hi:
        mid = (lo + hi) // 2

        if x == arr[mid] and (mid == 0 or x != arr[mid - 1]):
            return mid

        elif x <= arr[mid]:
            hi = mid

        else:
            lo = mid + 1

    return -1


class TestFindFirstInSorted(unittest.TestCase):
    def test_find_first_in_sorted(self):
        self.assertEqual(find_first_in_sorted([1, 2, 4, 4, 5], 4), 2)
        self.assertEqual(find_first_in_sorted([1, 1, 1, 1, 1], 1), 0)
        self.assertEqual(find_first_in_sorted([3, 5, 7, 9], 8), -1)
        self.assertEqual(find_first_in_sorted([], 4), -1)
        self.assertEqual(find_first_in_sorted([2, 4, 6, 8, 10], 1), -1)


if __name__ == "__main__":
    unittest.main()
