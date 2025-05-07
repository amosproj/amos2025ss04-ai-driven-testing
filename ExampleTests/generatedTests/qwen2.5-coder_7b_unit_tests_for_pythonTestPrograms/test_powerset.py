import unittest


def powerset(arr):
    if arr:
        first, *rest = arr
        rest_subsets = powerset(rest)
        return rest_subsets + [[first] + subset for subset in rest_subsets]
    else:
        return [[]]


class TestPowerset(unittest.TestCase):
    def test_empty_array(self):
        self.assertEqual(powerset([]), [[]])

    def test_single_element(self):
        self.assertEqual(powerset([1]), [[], [1]])

    def test_two_elements(self):
        self.assertEqual(powerset([1, 2]), [[], [2], [1], [1, 2]])

    def test_three_elements(self):
        self.assertEqual(
            powerset([1, 2, 3]),
            [[], [3], [2], [2, 3], [1], [1, 3], [1, 2], [1, 2, 3]],
        )


if __name__ == "__main__":
    unittest.main()
