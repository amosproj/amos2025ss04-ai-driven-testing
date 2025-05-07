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

    if len(arr) == 0 or len(arr) == 1:
        return arr
    else:
        middle = len(arr) // 2
        left = mergesort(arr[:middle])
        right = mergesort(arr[middle:])
        return merge(left, right)


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

    if len(arr) == 1 or len(arr) == 0:
        return arr
    else:
        middle = len(arr) // 2
        left = mergesort(arr[:middle])
        right = mergesort(arr[middle:])
        return merge(left, right)


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
from unittest import TestCase


class TestMergeSort(TestCase):
    def test_mergesort(self):
        # Test case 1: Empty array
        arr = []
        self.assertEqual([], mergesort(arr))

        # Test case 2: Single-element array
        arr = [5]
        self.assertEqual([5], mergesort(arr))

        # Test case 3: Already sorted array
        arr = [1, 2, 3, 4, 5]
        self.assertEqual([1, 2, 3, 4, 5], mergesort(arr))

        # Test case 4: Unsorted array
        arr = [5, 2, 7, 4, 3, 8, 6, 1]
        sorted_arr = [1, 2, 3, 4, 5, 6, 7, 8]
        self.assertEqual(sorted_arr, mergesort(arr))


if __name__ == "__main__":
    unittest.main()
