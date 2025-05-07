import unittest


def quicksort(arr):
    if not arr:
        return []

    pivot = arr[0]
    lesser = quicksort([x for x in arr[1:] if x <= pivot])
    greater = quicksort([x for x in arr[1:] if x > pivot])
    return lesser + [pivot] + greater


class TestQuicksort(unittest.TestCase):
    def test_empty_array(self):
        self.assertEqual(quicksort([]), [])

    def test_single_element_array(self):
        self.assertEqual(quicksort([5]), [5])

    def test_already_sorted_array(self):
        self.assertEqual(quicksort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_reverse_sorted_array(self):
        self.assertEqual(quicksort([5, 4, 3, 2, 1]), [1, 2, 3, 4, 5])

    def test_array_with_duplicates(self):
        self.assertEqual(
            quicksort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]),
            [1, 2, 3, 4, 5, 5, 5, 6, 9],
        )

    def test_array_with_negative_numbers(self):
        self.assertEqual(
            quicksort([-5, -2, 0, 3, 8, -1]), [-5, -2, -1, 0, 3, 8]
        )


if __name__ == "__main__":
    unittest.main()
