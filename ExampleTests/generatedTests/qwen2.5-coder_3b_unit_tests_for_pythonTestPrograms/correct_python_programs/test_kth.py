import unittest

class TestKth(unittest.TestCase):
    def test_kth(self):
        # Test case 1: Basic scenario with a middle element
        arr = [3, 6, 8, 10, 1, 2]
        k = 2
        self.assertEqual(kth(arr, k), 6)

        # Test case 2: When k is less than the number of elements less than the pivot
        arr = [5, 4, 3, 2, 1]
        k = 1
        self.assertEqual(kth(arr, k), 5)

        # Test case 3: When k is greater than or equal to the number of elements less than or equal to the pivot
        arr = [10, 9, 8, 7, 6, 5]
        k = 4
        self.assertEqual(kth(arr, k), 5)

        # Test case 4: When k is equal to the index of the pivot
        arr = [1, 2, 3, 4, 5, 6]
        k = 3
        self.assertEqual(kth(arr, k), 3)

        # Test case 5: Single element array
        arr = [7]
        k = 0
        self.assertEqual(kth(arr, k), 7)

        # Test case 6: Empty array (though this function will raise an exception)
        # arr = []
        # k = 0
        # with self.assertRaises(IndexError):
        #     kth(arr, k)

if __name__ == '__main__':
    unittest.main()