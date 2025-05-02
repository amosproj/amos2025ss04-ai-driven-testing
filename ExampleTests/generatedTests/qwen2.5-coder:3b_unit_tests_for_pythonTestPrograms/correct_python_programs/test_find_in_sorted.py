import unittest

def find_in_sorted(arr, x):
    def binsearch(start, end):
        if start == end:
            return -1
        mid = start + (end - start) // 2
        if x < arr[mid]:
            return binsearch(start, mid)
        elif x > arr[mid]:
            return binsearch(mid + 1, end)
        else:
            return mid

    return binsearch(0, len(arr))

class TestFindInSorted(unittest.TestCase):
    def test_find_in_sorted(self):
        self.assertEqual(find_in_sorted([1, 2, 3, 4, 5], 3), 2)
        self.assertEqual(find_in_sorted([1, 2, 3, 4, 5], 6), -1)
        self.assertEqual(find_in_sorted([5, 7, 9, 11, 13], 11), 3)
        self.assertEqual(find_in_sorted([1, 3, 5, 7, 9], 2), -1)
        self.assertEqual(find_in_sorted([10], 10), 0)
        self.assertEqual(find_in_sorted([], 5), -1)

if __name__ == '__main__':
    unittest.main()