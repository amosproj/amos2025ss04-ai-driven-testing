import unittest

class TestMergeSort(unittest.TestCase):

    def test_empty_array(self):
        self.assertEqual(mergesort([]), [])

    def test_single_element_array(self):
        self.assertEqual(mergesort([5]), [5])

    def test_already_sorted_array(self):
        self.assertEqual(mergesort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_reverse_sorted_array(self):
        self.assertEqual(mergesort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_unsorted_array(self):
        self.assertEqual(mergesort([3, 1, 4, 1, 5, 9, 2, 6]), [1, 2, 3, 4, 5, 6, 9])

    def test_array_with_duplicates(self):
        self.assertEqual(mergesort([5, 2, 8, 1, 9, 2, 5]), [1, 2, 2, 5, 5, 8, 9])

    def test_large_unsorted_array(self):
        arr = [5, 2, 8, 1, 9, 2, 5, 3, 7, 1, 6, 4, 8, 2, 9, 3, 7, 5, 1, 8, 4, 6, 3, 2, 1]
        expected = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 7, 7, 8, 8, 9, 9]
        self.assertEqual(mergesort(arr), expected)


if __name__ == '__main__':
    unittest.main()