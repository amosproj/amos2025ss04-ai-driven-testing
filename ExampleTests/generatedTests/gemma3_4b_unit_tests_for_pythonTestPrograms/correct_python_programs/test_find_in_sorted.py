def find_in_sorted(arr, x):
    def binsearch(start, end):
        if start == end:
            return -1
        mid = start + (end - start) // 2
        if x < arr[mid]:
            return binsearch(start, mid)
        elif x > arr[mid]:
            return binsearch(mid + 1, end)
        else:
            return mid

    return binsearch(0, len(arr))

import unittest

class TestFindInSorted(unittest.TestCase):

    def test_empty_array(self):
        self.assertEqual(find_in_sorted([], 5), -1)

    def test_element_found_at_beginning(self):
        self.assertEqual(find_in_sorted([2, 5, 7, 8, 10], 2), 0)

    def test_element_found_in_middle(self):
        self.assertEqual(find_in_sorted([2, 5, 7, 8, 10], 7), 2)

    def test_element_found_at_end(self):
        self.assertEqual(find_in_sorted([2, 5, 7, 8, 10], 10), 4)

    def test_element_not_found(self):
        self.assertEqual(find_in_sorted([2, 5, 7, 8, 10], 1), -1)

    def test_single_element_array_found(self):
        self.assertEqual(find_in_sorted([5], 5), 0)

    def test_element_greater_than_max(self):
        self.assertEqual(find_in_sorted([2, 5, 7, 8, 10], 11), -1)

    def test_element_less_than_min(self):
        self.assertEqual(find_in_sorted([2, 5, 7, 8, 10], 1), -1)


if __name__ == '__main__':
    unittest.main()