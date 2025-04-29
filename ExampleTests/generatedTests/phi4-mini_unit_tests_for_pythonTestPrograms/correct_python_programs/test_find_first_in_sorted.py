import unittest


def find_first_in_sorted(arr, x):
    lo = 0
    hi = len(arr)

    while lo + 1 <= hi:
        mid = (lo + hi) // 2

        if x == arr[mid] and (mid == 0 or x != arr[mid - 1]):
            return mid

        elif x <= arr[mid]:
            hi = mid

        else:
            lo = mid + 1

    return -1


class TestFindFirstInSorted(unittest.TestCase):

    def test_find_first_in_sorted(self):
        self.assertEqual(find_first_in_sorted([10, 20, 30], 20), 1)
        self.assertEqual(find_first_in_sorted([5, 7, 9], 6), -1)

    def test_edge_case_empty_list(self):
        with self.assertRaises(IndexError):
            find_first_in_sorted([], 0)

    def test_single_element_match(self):
        arr = [4]
        x = 4
        result = find_first_in_sorted(arr, x)
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()