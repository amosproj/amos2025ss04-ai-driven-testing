def subsequences(a, b, k):
    if k == 0:
        return [[]]

    ret = []
    for i in range(a, b + 1 - k):
        ret.extend([i] + rest for rest in subsequences(i + 1, b, k - 1))

    return ret


# Please generate a test class with unit tests for the above code using unittest. Return a python file containing the original code plus the test so that I just need to run the resulting file and i can see if the tests go through
import unittest


class TestSubsequences(unittest.TestCase):
    def test_empty_subsequences(self):
        self.assertEqual(subsequences(1, 3, 0), [[]])
        self.assertEqual(subsequences(1, 3, 1), [[1]])
        self.assertEqual(subsequences(1, 3, 2), [[1, 2], [1, 3]])
        self.assertEqual(subsequences(1, 3, 3), [[1, 2, 3]])

    def test_single_element_subsequences(self):
        self.assertEqual(subsequences(1, 3, 1), [[1]])
        self.assertEqual(subsequences(2, 4, 1), [[2], [3], [4]])

    def test_longer_ranges(self):
        self.assertEqual(
            subsequences(1, 5, 2),
            [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]],
        )
        self.assertEqual(
            subsequences(2, 6, 3),
            [
                [2, 3, 4],
                [2, 3, 5],
                [2, 3, 4],
                [2, 3, 5],
                [2, 3, 4],
                [2, 4, 5],
                [3, 4, 5],
            ],
        )


if __name__ == "__main__":
    unittest.main()
