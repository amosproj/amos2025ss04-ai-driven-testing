import sys
from unittest import TestCase
from itertools import combinations


def powerset(arr):
    if arr:
        first, *rest = arr
        rest_subsets = powerset(rest)
        return rest_subsets + [[first] + subset for subset in rest_subsets]
    else:
        return [[]]


class TestPowerset(TestCase):
    def test_powerset_empty(self):
        self.assertEqual(powerset([]), [[]])

    def test_powerset_single_element(self):
        expected = [["a"], []]
        actual = powerset(["a"])
        self.assertListEqual(actual, expected)

    def test_powerset_two_elements(self):
        expected = [[], ["a"], ["b"], ["a", "b"]]
        actual = powerset(["a", "b"])
        self.assertListEqual(actual, expected)

    def test_powerset_three_elements(self):
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
        actual = powerset(["a", "b", "c"])
        self.assertListEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
