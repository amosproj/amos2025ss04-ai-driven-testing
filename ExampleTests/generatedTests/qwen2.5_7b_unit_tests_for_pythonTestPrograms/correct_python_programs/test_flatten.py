def flatten(arr):
    for x in arr:
        if isinstance(x, list):
            for y in flatten(x):
                yield y
        else:
            yield x


import unittest


class TestFlattenFunction(unittest.TestCase):
    def test_flatten(self):
        self.assertEqual(
            list(flatten([1, [2, [3, 4], [[5]]], 6])), [1, 2, 3, 4, 5, 6]
        )
        self.assertEqual(
            list(flatten([[1, 2], 3, [4, [5]], 6])), [1, 2, 3, 4, 5, 6]
        )
        self.assertEqual(list(flatten([])), [])
        self.assertEqual(list(flatten([[], [], []])), [])
        self.assertEqual(list(flatten([[[[[]]]]])), [])


if __name__ == "__main__":
    unittest.main()
