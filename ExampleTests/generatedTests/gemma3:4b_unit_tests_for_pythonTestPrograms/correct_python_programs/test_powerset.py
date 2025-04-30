import unittest

def powerset(arr):
    if arr:
        first, *rest = arr
        rest_subsets = powerset(rest)
        return [[first] + subset for subset in rest_subsets] + rest_subsets
    else:
        return [[]]

class TestPowerset(unittest.TestCase):

    def test_empty_array(self):
        self.assertEqual(powerset([]), [[]])

    def test_single_element_array(self):
        self.assertEqual(powerset([1]), [[1]])

    def test_two_element_array(self):
        self.assertEqual(set(powerset([1, 2]))
                         == set([[], [1], [2], [1, 2]]))

    def test_three_element_array(self):
        expected = [[], [1], [2], [1, 2], [1, 3], [2, 3], [1, 2, 3], [1, 3, 4], [2, 3, 4], [1, 2, 3, 4]]
        self.assertEqual(set(powerset([1, 2, 3])) == set(expected))


if __name__ == '__main__':
    unittest.main()