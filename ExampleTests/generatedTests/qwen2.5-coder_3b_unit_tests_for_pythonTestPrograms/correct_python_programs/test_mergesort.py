import unittest

class TestMergesort(unittest.TestCase):
    def test_mergesort_empty(self):
        self.assertEqual(mergesort([]), [])

    def test_mergesort_single_element(self):
        self.assertEqual(mergesort([1]), [1])

    def test_mergesort_sorted_list(self):
        self.assertEqual(mergesort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_mergesort_unsorted_list(self):
        self.assertEqual(mergesort([5, 3, 8, 4, 2]), [2, 3, 4, 5, 8])

    def test_mergesort_large_list(self):
        arr = [i for i in range(1000)]
        sorted_arr = mergesort(arr)
        self.assertEqual(sorted_arr, list(range(1000)))

if __name__ == '__main__':
    unittest.main()