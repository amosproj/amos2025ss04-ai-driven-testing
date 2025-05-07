import unittest
from mergesort import mergesort


class Testmergesort(unittest.TestCase):
    def test_empty_array(self):
        arr = []
        sorted_arr = mergesort(arr)
        self.assertEqual(sorted_arr, arr)

    def test_single_element(self):
        arr = [5]
        sorted_arr = mergesort(arr)
        self.assertEqual(sorted_arr, arr)

    def test_merging_sorted_arrays(self):
        # Split the array into two halves
        mid = len([1, 2, 3, 4]) // 2
        left = [1, 2][:mid]
        right = [1, 2][mid:]

        # Sort each half (though they are already sorted)
        sorted_left = mergesort(left)
        sorted_right = mergesort(right)

        # Merge the two sorted arrays
        merged = []
        i = j = 0
        while i < len(sorted_left) and j < len(sorted_right):
            if sorted_left[i] < sorted_right[j]:
                merged.append(sorted_left[i])
                i += 1
            else:
                merged.append(sorted_right[j])
                j += 1
        while i < len(sorted_left):
            merged.append(sorted_left[i])
            i += 1
        while j < len(sorted_right):
            merged.append(sorted_right[j])
            j += 1

        self.assertEqual(merged, sorted([left + right]))


if __name__ == "__main__":
    unittest.main()
