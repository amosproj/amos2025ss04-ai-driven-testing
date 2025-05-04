import unittest

class TestBucketsort(unittest.TestCase):
    def test_bucketsort(self):
        # Test case 1: Simple sorting with distinct elements
        arr = [3, 6, 8, 10, 1, 2, 1]
        k = max(arr) + 1
        expected = [1, 1, 2, 3, 6, 8, 10]
        self.assertEqual(bucketsort(arr, k), expected)

        # Test case 2: Sorting with repeated elements
        arr = [4, 4, 5, 5, 6, 7, 7, 8, 9]
        k = max(arr) + 1
        expected = [4, 4, 5, 5, 6, 7, 7, 8, 9]
        self.assertEqual(bucketsort(arr, k), expected)

        # Test case 3: Sorting with negative numbers
        arr = [-2, -3, -1, 0, 1, 2, 3, 4]
        k = max(abs(min(arr)), max(abs(max(arr)))) + 1
        expected = [-3, -2, -1, 0, 1, 2, 3, 4]
        self.assertEqual(bucketsort(arr, k), expected)

        # Test case 4: Sorting with empty list
        arr = []
        k = 1
        expected = []
        self.assertEqual(bucketsort(arr, k), expected)

if __name__ == '__main__':
    unittest.main()