import unittest

from find_in_sorted import find_in_sorted


class TestfindInSorted(unittest.TestCase):
    def test_find_in_sorted(self):
        # Test when element is found in the list
        self.assertEqual(find_in_sorted([1, 2, 3, 4, 5], 3), 2)
        self.assertEqual(find_in_sorted([1, 2, 3, 4, 5], 1), 0)
        self.assertEqual(find_in_sorted([1, 2, 3, 4, 5], 5), 4)
        
        # Test when element is not found in the list
        self.assertEqual(find_in_sorted([1, 2, 3, 4, 5], 6), -1)
        self.assertEqual(find_in_sorted([1, 2, 3, 4, 5], 0), -1)
        
        # Test with empty list
        self.assertEqual(find_in_sorted([], 1), -1)

if __name__ == '__main__':
    unittest.main()