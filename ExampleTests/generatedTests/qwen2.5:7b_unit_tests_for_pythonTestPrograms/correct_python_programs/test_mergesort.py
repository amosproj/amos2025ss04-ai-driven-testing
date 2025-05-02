def mergesort(arr):
    def merge(left, right):
        result = []
        i = 0
        j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        result.extend(left[i:] or right[j:])
        return result

    if len(arr) < 2:
        return arr
    else:
        middle = len(arr) // 2
        left = mergesort(arr[:middle])
        right = mergesort(arr[middle:])
        return merge(left, right)

import unittest

class TestMergeSort(unittest.TestCase):
    
    def test_merge_sort_empty_array(self):
        self.assertEqual(mergesort([]), [])

    def test_merge_sort_single_element(self):
        self.assertEqual(mergesort([5]), [5])

    def test_merge_sort_two_elements(self):
        self.assertEqual(mergesort([5, 3]), [3, 5])
        self.assertEqual(mergesort([3, 5]), [3, 5])

    def test_merge_sort_three_elements(self):
        self.assertEqual(mergesort([5, 3, 1]), [1, 3, 5])
        self.assertEqual(mergesort([3, 5, 1]), [1, 3, 5])
        self.assertEqual(mergesort([1, 3, 5]), [1, 3, 5])

    def test_merge_sort_four_elements(self):
        self.assertEqual(mergesort([4, 2, 1, 3]), [1, 2, 3, 4])
        self.assertEqual(mergesort([1, 4, 2, 3]), [1, 2, 3, 4])

    def test_merge_sort_large_random_array(self):
        import random
        arr = list(range(100))
        random.shuffle(arr)
        sorted_arr = mergesort(arr)
        self.assertEqual(sorted_arr, list(range(100)))

if __name__ == '__main__':
    unittest.main()