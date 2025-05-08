import unittest


class Testbucketsoort(unittest.TestCase):

    def test_bucketsort(self, arr, k):
        counts = [0] * k
        for x in arr:
            counts[x] += 1
        sorted_arr = []
        for i, count in enumerate(counts):
            if count > 0:
                sorted_arr.extend([i] * count)
        self.assertEqual(sorted_arr, expected_result)

    def test_bucketsort_empty(self, arr, k):
        if not arr:
            return True
        counts = [0] * k
        for x in arr:
            counts[x] += 1
        sorted_arr = []
        for i, count in enumerate(counts):
            if count > 0:
                sorted_arr.extend([i] * count)
        self.assertEqual(sorted_arr, expected_empty)

    def test_bucketsort_single(self, arr, k):
        if len(arr) == 1:
            return True
        counts = [0] * k
        for x in arr:
            counts[x] += 1
        sorted_arr = []
        for i, count in enumerate(counts):
            if count > 0:
                sorted_arr.extend([i] * count)
        self.assertEqual(sorted_arr, expected_single)

if __name__ == "__main__":
    unittest.main()