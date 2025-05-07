import unittest


def kth(arr, k):
    pivot = arr[0]
    below = [x for x in arr if x < pivot]
    above = [x for x in arr if x > pivot]

    num_less = len(below)
    num_lessoreq = len(arr) - len(above)

    if k < num_less:
        return kth(below, k)
    elif k >= num_lessoreq:
        return kth(above, k - num_lessoreq)
    else:
        return pivot


class TestKth(unittest.TestCase):
    def test_empty_array(self):
        with self.assertRaises(IndexError):
            kth([], 1)

    def test_k_less_than_length(self):
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        k = 3
        self.assertEqual(kth(arr, k), 3)

    def test_k_equal_to_length(self):
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        k = 8
        self.assertEqual(kth(arr, k), 6)

    def test_k_greater_than_length(self):
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        k = 9
        self.assertEqual(kth(arr, k), 9)

    def test_k_is_first_element(self):
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        k = 1
        self.assertEqual(kth(arr, k), 1)

    def test_k_is_last_element(self):
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        k = 8
        self.assertEqual(kth(arr, k), 6)

    def test_k_is_middle_element(self):
        arr = [3, 1, 4, 1, 5, 9, 2, 6]
        k = 5
        self.assertEqual(kth(arr, k), 5)

    def test_duplicate_elements(self):
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 1, 1]
        k = 5
        self.assertEqual(kth(arr, k), 5)

    def test_already_sorted_array(self):
        arr = [1, 2, 3, 4, 5]
        k = 3
        self.assertEqual(kth(arr, k), 3)

    def test_reverse_sorted_array(self):
        arr = [5, 4, 3, 2, 1]
        k = 3
        self.assertEqual(kth(arr, k), 3)


if __name__ == "__main__":
    unittest.main()
