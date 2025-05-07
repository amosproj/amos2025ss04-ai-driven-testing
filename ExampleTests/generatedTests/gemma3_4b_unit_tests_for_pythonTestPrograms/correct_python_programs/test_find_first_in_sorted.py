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


class TestFindFirstInSorted(unittest.TestCase):
    def test_empty_array(self):
        self.assertEqual(find_first_in_sorted([], 5), -1)

    def test_element_at_beginning(self):
        self.assertEqual(find_first_in_sorted([2, 3, 4, 5], 2), 0)

    def test_element_at_end(self):
        self.assertEqual(find_first_in_sorted([2, 3, 4, 5], 5), 3)

    def test_element_not_present(self):
        self.assertEqual(find_first_in_sorted([2, 3, 4, 5], 1), -1)
        self.assertEqual(find_first_in_sorted([2, 3, 4, 5], 6), -1)

    def test_multiple_occurrences(self):
        self.assertEqual(find_first_in_sorted([1, 2, 2, 2, 3], 2), 1)

    def test_single_element_array(self):
        self.assertEqual(find_first_in_sorted([5], 5), 0)
        self.assertEqual(find_first_in_sorted([5], 6), -1)

    def test_duplicate_first_element(self):
        self.assertEqual(find_first_in_sorted([2, 2, 2, 2, 3], 2), 0)

    def test_large_array(self):
        arr = list(range(1000))
        self.assertEqual(find_first_in_sorted(arr, 500), 499)
        self.assertEqual(find_first_in_sorted(arr, 999), 998)


if __name__ == "__main__":
    unittest.main()
