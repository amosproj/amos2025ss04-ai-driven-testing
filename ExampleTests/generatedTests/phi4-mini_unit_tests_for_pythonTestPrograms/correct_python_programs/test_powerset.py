import unittest


def powerset(arr):
    """
    Generates all possible subsets (the power set) of an array.

    Parameters:
        arr: list - An input list for which we want to generate its powerset.

    Returns:
        List[List]: A 2D list where each sublist is a subset in the powerset
                     including empty sets and single-element lists up till
                     full set itself represented as nested sublists.

    Example usage:

        >>> powerset([1, 2])
        [[], [1], [2], [1, 2]]
    """
    if arr:
        first, *rest = arr
        rest_subsets = powerset(rest)
        return [[first] + subset for subset in rest_subsets] + rest_subsets
    else:
        return [[]]


class TestPowerSet(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(powerset([]), [[]])

    def test_single_element_list(self):
        self.assertEqual(powerset([1]), [[1]])

    def test_multiple_elements_no_duplicates(self):
        result = powerset([1, 2])
        expected = [[], [1], [2], [1, 2]]
        for exp in expected:
            self.assertIn(exp, result)

    def test_all_elements_list(self):
        # Test with a list containing all unique elements
        result = powerset(["a", "b", "c"])
        expected = [
            [],
            ["a"],
            ["b"],
            ["c"],
            ["a", "b"],
            ["a", "c"],
            ["b", "c"],
            ["a", "b", "c"],
        ]

        for exp in expected:
            self.assertIn(exp, result)


if __name__ == "__main__":
    unittest.main()
