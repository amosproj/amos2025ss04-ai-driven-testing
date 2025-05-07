def quicksort(arr):
    if not arr:
        return []

    pivot = arr[0]
    lesser = quicksort([x for x in arr[1:] if x < pivot])
    greater = quicksort([x for x in arr[1:] if x >= pivot])
    return lesser + [pivot] + greater


import unittest


class TestQuicksort(unittest.TestCase):
    def test_quicksort_empty(self):
        self.assertEqual(quicksort([]), [])

    def test_quicksort_single_element(self):
        self.assertEqual(quicksort([5]), [5])

    def test_quicksort_sorted(self):
        self.assertEqual(quicksort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_quicksort_unsorted(self):
        self.assertEqual(
            quicksort([5, 3, 9, 0, 6, 7, 8]), [0, 3, 5, 6, 7, 8, 9]
        )


if __name__ == "__main__":
    unittest.main()
