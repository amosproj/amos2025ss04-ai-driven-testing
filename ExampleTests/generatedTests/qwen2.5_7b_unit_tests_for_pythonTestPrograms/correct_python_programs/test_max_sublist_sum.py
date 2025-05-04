def max_sublist_sum(arr):
    max_ending_here = 0
    max_so_far = 0

    for x in arr:
        max_ending_here = max(0, max_ending_here + x)
        max_so_far = max(max_so_far, max_ending_here)

    return max_so_far


import unittest

class TestMaxSublistSum(unittest.TestCase):
    
    def test_max_sublist_sum(self):
        self.assertEqual(max_sublist_sum([1, -2, 3, 4, -1, 2, 1, -5, 4]), 6)
        self.assertEqual(max_sublist_sum([-2, -3, -1]), 0)
        self.assertEqual(max_sublist_sum([]), 0)
        self.assertEqual(max_sublist_sum([5, -7, 3, 9, -2]), 13)
        self.assertEqual(max_sublist_sum([1, 2, 3, 4, -10, 10]), 10)

if __name__ == '__main__':
    unittest.main()