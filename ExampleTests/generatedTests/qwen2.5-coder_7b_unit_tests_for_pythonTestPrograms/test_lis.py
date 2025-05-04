import unittest

def lis(arr):
    ends = {}
    longest = 0

    for i, val in enumerate(arr):

        prefix_lengths = [j for j in range(1, longest + 1) if arr[ends[j]] < val]

        length = max(prefix_lengths) if prefix_lengths else 0

        if length == longest or val < arr[ends[length + 1]]:
            ends[length + 1] = i
            longest = max(longest, length + 1)

    return longest

class TestLIS(unittest.TestCase):
    def test_lis_empty_array(self):
        self.assertEqual(lis([]), 0)

    def test_lis_single_element(self):
        self.assertEqual(lis([5]), 1)

    def test_lis_increasing_sequence(self):
        self.assertEqual(lis([1, 2, 3, 4, 5]), 5)

    def test_lis_decreasing_sequence(self):
        self.assertEqual(lis([5, 4, 3, 2, 1]), 1)

    def test_lis_mixed_sequence(self):
        self.assertEqual(lis([3, 10, 2, 11, 15]), 4)

    def test_lis_with_duplicates(self):
        self.assertEqual(lis([7, 7, 7, 7, 7]), 1)

if __name__ == '__main__':
    unittest.main()