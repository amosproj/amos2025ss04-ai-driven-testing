import unittest

from kheapsort import kheapsort


class TestKheapSort(unittest.TestCase):
    def test_kheapsort(self):
        # Test case 1: Basic test with ascending order input
        arr = [3, 5, 2, 4, 6]
        expected = [2, 3, 4, 5, 6]
        result = list(kheapsort(arr, k=3))
        self.assertEqual(result, expected)

        # Test case 2: Basic test with descending order input
        arr = [6, 5, 4, 3, 2]
        expected = [2, 3, 4, 5, 6]
        result = list(kheapsort(arr, k=3))
        self.assertEqual(result, expected)

        # Test case 3: Single element in the heap
        arr = [7]
        expected = [7]
        result = list(kheapsort(arr, k=1))
        self.assertEqual(result, expected)

        # Test case 4: Empty input
        arr = []
        expected = []
        result = list(kheapsort(arr, k=3))
        self.assertEqual(result, expected)

        # Test case 5: All elements are the same
        arr = [8] * 10
        expected = [8] * 10
        result = list(kheapsort(arr, k=3))
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
