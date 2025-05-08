import unittest


def subsequences(a, b, k):
    if k == 0:
        return [[]]

    ret = []
    for i in range(a, b + 1 - k):
        ret.extend([i] + rest for rest in subsequences(i + 1, b, k - 1))

    return ret


class TestSubsequences(unittest.TestCase):
    def test_subsequences_with_k_0(self):
        self.assertEqual(subsequences(1, 5, 0), [[]])

    def test_subsequences_with_k_1(self):
        self.assertEqual(subsequences(1, 5, 1), [[1], [2], [3], [4], [5]])

    def test_subsequences_with_k_2(self):
        self.assertEqual(
            subsequences(1, 5, 2),
            [[1, 3], [1, 4], [1, 5], [2, 4], [2, 5], [3, 5]],
        )

    def test_subsequences_with_negative_a_and_b(self):
        self.assertEqual(subsequences(-3, -1, 2), [[-3, -1]])

    def test_subsequences_with_k_greater_than_range_length(self):
        self.assertEqual(subsequences(1, 3, 4), [])


if __name__ == "__main__":
    unittest.main()
