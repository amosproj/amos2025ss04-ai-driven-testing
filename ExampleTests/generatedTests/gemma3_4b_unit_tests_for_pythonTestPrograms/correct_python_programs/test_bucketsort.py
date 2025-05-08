import unittest


def bucketsort(arr, k):
    counts = [0] * k
    for x in arr:
        counts[x] += 1

    sorted_arr = []
    for i, count in enumerate(counts):
        sorted_arr.extend([i] * count)

    return sorted_arr


class TestBucketSort(unittest.TestCase):
    def test_empty_array(self):
        self.assertEqual(bucketsort([], 0), [])

    def test_single_element(self):
        self.assertEqual(bucketsort([5], 5), [5])

    def test_basic_sorting(self):
        arr = [10, 4, 5, 8, 1, 9, 7, 2, 6, 3, 8, 1, 3, 5, 8]
        k = 10
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        self.assertEqual(bucketsort(arr, k), expected)

    def test_duplicate_elements(self):
        arr = [4, 6, 2, 8, 4, 8, 2, 4, 6, 8]
        k = 9
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertEqual(bucketsort(arr, k), expected)

    def test_k_equals_max_value(self):
        arr = [1, 2, 3, 4, 5]
        k = 5
        expected = [1, 2, 3, 4, 5]
        self.assertEqual(bucketsort(arr, k), expected)

    def test_k_is_one(self):
        arr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
        k = 1
        expected = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assertEqual(bucketsort(arr, k), expected)


if __name__ == "__main__":
    unittest.main()
