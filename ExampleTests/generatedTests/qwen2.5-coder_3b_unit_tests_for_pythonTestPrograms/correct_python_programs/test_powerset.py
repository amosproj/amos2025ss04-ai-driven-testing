import unittest


def powerset(arr):
    if arr:
        first, *rest = arr
        rest_subsets = powerset(rest)
        return [[first] + subset for subset in rest_subsets] + rest_subsets
    else:
        return [[]]


class TestPowerset(unittest.TestCase):
    def test_powerset_empty(self):
        self.assertEqual(powerset([]), [[]])

    def test_powerset_single_element(self):
        self.assertEqual(powerset([1]), [[], [1]])

    def test_powerset_multiple_elements(self):
        self.assertEqual(powerset([1, 2]), [[], [1], [2], [1, 2]])

    def test_powerset_duplicated_elements(self):
        self.assertEqual(powerset([1, 1]), [[], [1], [1, 1]])


if __name__ == "__main__":
    unittest.main()
