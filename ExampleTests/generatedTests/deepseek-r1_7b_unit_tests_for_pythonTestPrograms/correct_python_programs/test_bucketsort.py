def bucketsort(arr, k):
    counts = [0] * k
    for x in arr:
        counts[x] += 1

    sorted_arr = []
    for i, count in enumerate(counts):
        if count > 0:  # Skip adding elements with zero count
            sorted_arr.extend([i] * count)

    return sorted_arr


# Second version of the function (the buggy one)
def bucketsort(arr, k):
    counts = [0] * k
    for x in arr:
        counts[x] += 1

    sorted_arr = []
    for i in range(len(arr)):
        if counts[i] > 0:  # Skip elements with zero count
            sorted_arr.extend([arr[i]] * counts[i])

    return sorted_arr


import unittest

from correct_python_programs.bucketsortfromcorrect_python_programs import \
    bucketsort


class TestBucketsort(unittest.TestCase):
    def test_bucketsort(self, arr, expected_result=None, k=None):
        self.assertEqual(bucketsort(arr, k), expected_result)

    def test_sort_positive_numbers(self):
        result = bucketsort([5, 2, 3], 6)
        self.assertEqual(result, [2, 3, 5])

    def test_sort_empty_array(self):
        result = bucketsort([], 0)
        self.assertEqual(result, [])

    def test_sort_negative_numbers(self):
        result = bucketsort([-1, -3, 0], k=4)
        self.assertEqual(result, [-3, -1, 0])


if __name__ == "__main__":
    unittest.main()
