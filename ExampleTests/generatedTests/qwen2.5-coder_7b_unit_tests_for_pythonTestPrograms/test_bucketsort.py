import unittest


def bucketsort(arr, k):
    counts = [0] * k
    for x in arr:
        counts[x] += 1

    sorted_arr = []
    for i, count in enumerate(counts):
        sorted_arr.extend([i] * count)

    return sorted_arr


class TestBucketsort(unittest.TestCase):
    def test_bucketsort_with_positive_numbers(self):
        self.assertEqual(
            bucketsort([3, 6, 8, 10, 1, 2, 1], 10), [1, 1, 2, 3, 6, 8, 10]
        )

    def test_bucketsort_with_duplicates(self):
        self.assertEqual(bucketsort([4, 1, 2, 2, 3, 1], 5), [1, 1, 2, 2, 3, 4])

    def test_bucketsort_with_empty_array(self):
        self.assertEqual(bucketsort([], 5), [])

    def test_bucketsort_with_single_element(self):
        self.assertEqual(bucketsort([7], 8), [7])

    def test_bucketsort_with_negative_numbers_and_zero(self):
        self.assertEqual(bucketsort([-1, -3, -2, 0, 4], 5), [-3, -2, -1, 0, 4])


if __name__ == "__main__":
    unittest.main()
