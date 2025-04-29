import unittest

class TestSubsequences(unittest.TestCase):
    def test_subsequences(self):
        # Test case 1: Empty list when k is 0
        self.assertEqual(sub subsequences(1, 3, 0), [[]])

        # Test case 2: Single element list when k is 1
        self.assertEqual(subsequences(1, 3, 1), [[1], [2], [3]])

        # Test case 3: All possible subsequences of length 2 from 1 to 4
        self.assertEqual(subsequences(1, 4, 2), [
            [1, 2],
            [1, 3],
            [1, 4],
            [2, 3],
            [2, 4],
            [3, 4]
        ])

        # Test case 4: All possible subsequences of length 3 from 1 to 5
        self.assertEqual(subsequences(1, 5, 3), [
            [1, 2, 3],
            [1, 2, 4],
            [1, 2, 5],
            [1, 3, 4],
            [1, 3, 5],
            [1, 4, 5],
            [2, 3, 4],
            [2, 3, 5],
            [2, 4, 5],
            [3, 4, 5]
        ])

        # Test case 5: Empty list when k is greater than the range
        self.assertEqual(subsequences(1, 3, 4), [])

if __name__ == '__main__':
    unittest.main()