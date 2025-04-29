def subsequences(a, b, k):
    if k == 0:
        return [[]]

    ret = []
    for i in range(a, b + 1 - k):
        ret.extend(
            [i] + rest for rest in subsequences(i + 1, b, k - 1)
        )

    return ret


import unittest
from itertools import permutations

class TestSubsequences(unittest.TestCase):

    def test_subsequences(self):
        self.assertEqual(subsequences(0, 3, 2), [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3], [2, 3]])

    def test_subsequences_k_zero(self):
        self.assertEqual(subsequences(0, 3, 0), [[]])

    def test_subsequences_empty_range(self):
        self.assertEqual(subsequences(5, 4, 2), [])

    def test_subsequences_large_range(self):
        result = subsequences(1, 6, 3)
        expected = [p for p in permutations(range(1, 7), 3)]
        self.assertCountEqual(result, expected)

if __name__ == '__main__':
    unittest.main()