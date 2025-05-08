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
        self.assertEqual(find_in_sorted([1, 2, 3, 4], 3), 2)

    def test_not_found_low_value(self):
        self.assertEqual(find_in_sorted([1, 2, 3, 4], -1), -1)

    def test_not_found_high_value(self):
        self.assertEqual(find_in_sorted([1, 2, 3, 4], 5), -1)

    def test_empty_list(self):
        empty_arr = []
        self.assertEqual(find_in_sorted(empty_arr, 0), -1)


if __name__ == "__main__":
    unittest.main()
