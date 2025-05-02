import unittest

def lis(arr):
    ends = {}
    longest = 0

    for i, val in enumerate(arr):

        prefix_lengths = [j for j in range(1, longest + 1) if arr[ends[j]] < val]

        length = max(prefix_lengths) if prefix_lengths else 0

        if length == longest or val < arr[ends[length + 1]]:
            ends[length + 1] = i
            longest = max(length + 1, longest)

    return longest

class TestLIS(unittest.TestCase):

    def test_empty_array(self):
        self.assertEqual(lis([]), 0)

    def test_single_element(self):
        self.assertEqual(lis([1]), 1)

    def test_example_1(self):
        self.assertEqual(lis([10, 9, 2, 5, 3, 7, 101, 18]), 4)

    def test_example_2(self):
        self.assertEqual(lis([0, 1, 0, 3, 2, 3]), 4)

    def test_example_3(self):
        self.assertEqual(lis([7, 7, 7, 7, 7, 7, 7]), 1)

    def test_example_4(self):
        self.assertEqual(lis([1,3,6,7,9,4,10,12,19]), 6)

    def test_example_5(self):
        self.assertEqual(lis([1,2,3,4,5]), 5)

    def test_example_6(self):
        self.assertEqual(lis([5,4,3,2,1]), 1)


if __name__ == '__main__':
    unittest.main()