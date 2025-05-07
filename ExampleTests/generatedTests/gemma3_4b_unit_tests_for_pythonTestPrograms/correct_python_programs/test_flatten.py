def flatten(arr):
    for x in arr:
        if isinstance(x, list):
            for y in flatten(x):
                yield y
        else:
            yield x


import unittest


class TestFlatten(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(list(flatten([])), [])

    def test_single_element(self):
        self.assertEqual(list(flatten([1])), [1])

    def test_list_of_numbers(self):
        self.assertEqual(list(flatten([1, 2, [3, 4], 5])), [1, 2, 3, 4, 5])

    def test_list_with_nested_lists(self):
        self.assertEqual(list(flatten([[1, 2], [3, [4, 5]]])), [1, 2, 3, 4, 5])

    def test_mixed_types(self):
        self.assertEqual(
            list(
                flatten([1, [2, "a"], [3, [4, "b"]]]),
            ),
            [1, 2, "a", 3, 4, "b"],
        )

    def test_deeply_nested_list(self):
        self.assertEqual(list(flatten([[1, [2, [3]]]])), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
