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

    if len(arr) <= 1:
        return arr
    else:
        middle = len(arr) // 2
        left = mergesort(arr[:middle])
        right = mergesort(arr[middle:])
        return merge(left, right)

class TestMergesort(unittest.TestCase):
    def test_empty_array(self):
        self.assertEqual(mergesort([]), [])

    def test_single_element_array(self):
        self.assertEqual(mergesort([5]), [5])

    def test_sorted_array(self):
        self.assertEqual(mergesort([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_unsorted_array(self):
        self.assertEqual(mergesort([3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]), [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9])

    def test_repeated_elements(self):
        self.assertEqual(mergesort([3, 3, 2, 1, 3, 3]), [1, 2, 3, 3, 3, 3])

if __name__ == '__main__':
    unittest.main()