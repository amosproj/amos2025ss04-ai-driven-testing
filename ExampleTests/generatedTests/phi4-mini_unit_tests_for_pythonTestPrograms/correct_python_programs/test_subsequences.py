import unittest


def subsequences(a, b, k):
    if k == 0:
        return [[]]

    ret = []
    for i in range(a, b + 1 - k):
        ret.extend([i] + rest for rest in subsequences(i + 1, b, k - 1))

    return ret


class TestSubsequences(unittest.TestCase):
    def test_subsequence_zero(self):
        self.assertEqual(subsequences(0, 10, 0), [[]])

    def test_no_valid_subsequences(self):
        self.assertEqual(subsequences(5, 7, 3), [])

    def test_single_number_subsequence(self):
        self.assertEqual(subsequences(4, 6, 1), [[4]])

    def test_multiple_numbers_subsequence(self):
        expected = [[2], [3], [4]]
        result = subsequences(5, 7, 2)
        sorted_result = sorted(
            result
        )  # Sorting to ensure order-independent comparison
        self.assertEqual(sorted_result, expected)

    def test_edge_case_large_k(self):
        with self.assertRaises(
            ValueError
        ):  # Assuming you want this function to raise an error for large k values.
            subsequences(0, 5, 6)


if __name__ == "__main__":
    unittest.main()
