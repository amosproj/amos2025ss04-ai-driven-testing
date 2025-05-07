import unittest


def quicksort(arr):
    if not arr:
        return []

    pivot = arr[0]
    lesser = quicksort([x for x in arr[1:] if x < pivot])
    greater = quicksort([x for x in arr[1:] if x >= pivot])
    return lesser + [pivot] + greater


class TestQuicksort(unittest.TestCase):
    def test_empty_array(self):
        self.assertEqual(quicksort([]), [])

    def test_single_element_array(self):
        self.assertEqual(quicksort([5]), [5])

    def test_sorted_array(self):
        self.assertEqual(quicksort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_reverse_sorted_array(self):
        self.assertEqual(quicksort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_unsorted_array(self):
        self.assertEqual(
            quicksort([3, 6, 8, 10, 1, 2, 1]), [1, 1, 2, 3, 6, 8, 10]
        )


if __name__ == "__main__":
    unittest.main()
