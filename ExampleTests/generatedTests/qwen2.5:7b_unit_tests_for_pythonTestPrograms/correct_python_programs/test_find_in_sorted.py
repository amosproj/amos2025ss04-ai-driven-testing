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


import unittest


class TestFindInSorted(unittest.TestCase):
    def test_binsearch(self):
        self.assertEqual(find_in_sorted([1, 2, 3, 4, 5], 3), 2)
        self.assertEqual(find_in_sorted([1, 2, 3, 4, 5], 6), -1)
        self.assertEqual(find_in_sorted([1, 2, 3, 4, 5], 1), 0)
        self.assertEqual(find_in_sorted([1, 2, 3, 4, 5], 5), 4)

    def test_empty_array(self):
        self.assertEqual(find_in_sorted([], 1), -1)

    def test_single_element(self):
        self.assertEqual(find_in_sorted([5], 5), 0)
        self.assertEqual(find_in_sorted([5], 6), -1)


if __name__ == '__main__':
    unittest.main()
```

To run this code, you can save it to a file (e.g., `test_find_in_sorted.py`) and execute it using the command:
```sh
python test_find_in_sorted.py