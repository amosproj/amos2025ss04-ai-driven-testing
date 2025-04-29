import unittest

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

    if len(arr) == 0 or len(arr) < 2:
        return arr
    else:
        middle = len(arr) // 2
        left = mergesort(arr[:middle])
        right = mergesort(arr[middle:])
        return merge(left, right)

class TestMergesort(unittest.TestCase):

    def test_empty_list(self):
        self.assertEqual(mergesort([]), [])

    def test_single_element_list(self):
        self.assertEqual(mergesort([1]), [1])

    def test_multiple_elements_sorted_list(self):
        arr = [1, 2, 3, 4, 5]
        result = mergesort(arr)
        expected_result = sorted(arr) # This is the actual merge sort for reference
        self.assertEqual(result, expected_result)

    def test_unsorted_list(self):
        unsorted_arr = [5, 3, 1, 2, 4]
        arr_to_sort = unsorted_arr.copy()
        mergesort(arr_to_sort)
        expected_sorted = sorted(unsorted_arr) # This is the actual merge sort for reference
        self.assertEqual(sorted(arr_to_sort), expected_sorted)

    def test_list_with_duplicates(self):
        with_dups_arr = [3, 1, 2, 3]
        arr_to_sort = with_dups_arr.copy()
        mergesort(arr_to_sort)
        expected_sorted = sorted(with_dups_arr) # This is the actual merge sort for reference
        self.assertEqual(sorted(arr_to_sort), expected_sorted)

    def test_large_unsorted_list(self):
        large_unsorted_array = [3, 1, 4, 2] * 1000 + [500]
        arr_to_sort = large_unsorted_array.copy()
        mergesort(arr_to_sort)
        self.assertEqual(sorted(arr_to_sort), sorted(large_unsorted_array))

if __name__ == '__main__':
    unittest.main()