import unittest


def flatten(arr):
    for x in arr:
        if isinstance(x, list):
            for y in flatten(x):
                yield y
        else:
            yield x


class TestFlatten(unittest.TestCase):
    def test_flatten_empty_list(self):
        self.assertEqual(list(flatten([])), [])

    def test_flatten_single_element(self):
        self.assertEqual(list(flatten([1])), [1])

    def test_flatten_nested_lists(self):
        self.assertEqual(
            list(flatten([1, [2, 3], [4, [5, 6]]])), [1, 2, 3, 4, 5, 6]
        )

    def test_flatten_mixed_elements(self):
        self.assertEqual(
            list(flatten([1, "a", [2, "b"], [3, ["c", 4]]])),
            [1, "a", 2, "b", 3, "c", 4],
        )


if __name__ == "__main__":
    unittest.main()
