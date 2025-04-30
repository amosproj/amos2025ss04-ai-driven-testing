import unittest

def quicksort(arr):
    """Sorts an array of numbers in ascending order."""
    if not arr:
        return []

    pivot = arr[0]
    lesser = quicksort([x for x in arr[1:] if x < pivot])
    greater = quicksort([x for x in arr[1:]])
    
    # Note that we now compare with the original condition, which does include equal values
    less_equal_pivot = [x for x in arr[1:] if x <= pivot]
    return lesser + less_equal_pivot + [pivot] + greater

class TestQuickSort(unittest.TestCase):

    def test_empty_list(self):
        self.assertEqual(quicksort([]), [])

    def test_single_element(self):
        self.assertEqual(quicksort([5]), [5])

    def test_sorted_input(self):
        self.assertEqual(quicksort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])
        
    def test_unsorted_input(self):
        unsorted = [3, 6, 8, 10, 1, 2, 1]
        self.assertEqual(quicksort(unsorted), sorted(sorted(unsorted)))

if __name__ == '__main__':
    unittest.main()