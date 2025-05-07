import unittest

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

class TestFindInSorted(unittest.TestCase):
    def test_empty_array(self):
        self.assertEqual(find_in_sorted([], 5), -1)

    def test_single_element_not_found(self):
        self.assertEqual(find_in_sorted([3], 2), -1)

    def test_single_element_found(self):
        self.assertEqual(find_in_sorted([3], 3), 0)

    def test_multiple_elements_not_found(self):
        self.assertEqual(find_in_sorted([1, 2, 4, 5, 6], 3), -1)

    def test_multiple_elements_found_at_start(self):
        self.assertEqual(find_in_sorted([1, 2, 4, 5, 6], 1), 0)

    def test_multiple_elements_found_in_middle(self):
        self.assertEqual(find_in_sorted([1, 2, 4, 5, 6], 4), 2)

    def test_multiple_elements_found_at_end(self):
        self.assertEqual(find_in_sorted([1, 2, 4, 5, 6], 6), 4)

if __name__ == '__main__':
    unittest.main()