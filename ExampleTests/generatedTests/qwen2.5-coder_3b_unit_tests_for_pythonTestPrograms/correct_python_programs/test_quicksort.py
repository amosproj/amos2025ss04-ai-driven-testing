import unittest


class TestQuicksort(unittest.TestCase):
    def test_quicksort_empty_list(self):
        self.assertEqual(quicksort([]), [])

    def test_quicksort_single_element(self):
        self.assertEqual(quicksort([5]), [5])

    def test_quicksort_sorted_list(self):
        self.assertEqual(quicksort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_quicksort_reversed_list(self):
        self.assertEqual(quicksort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_quicksort_unsorted_list(self):
        self.assertEqual(
            quicksort([3, 6, 8, 10, 1, 2, 1]), [1, 1, 2, 3, 6, 8, 10]
        )


if __name__ == "__main__":
    unittest.main()
