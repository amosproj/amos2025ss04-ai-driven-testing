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

    def test_flatten_single_element_nonlist(self):
        input_data = [42]
        expected_output = list(input_data)
        actual_output = list(flatten(input_data))
        self.assertEqual(actual_output, expected_output)

    def test_flatten_multiple_elements_listed_separately(self):
        input_data = [1, 2, [3], [[4]], [[[5]]]]
        flattened_result = flatten([input_data])
        expected_output = [1, 2, 3, 4, 5]
        actual_output = list(flatened_result)
        self.assertEqual(actual_output, expected_output)

    def test_flatten_nested_list(self):
        input_data = [[[0], 1], 2, 3]
        flattened_result = flatten([input_data])
        expected_output = [0, 1, 2, 3]
        actual_output = list(flattened_result)
        self.assertEqual(actual_output, expected_output)

    def test_flatten_complex_structure(self):
        input_data = [[[[[1]]]], [[[[]]]], [[]]]
        flattened_result = flatten([input_data])
        expected_output = [1]
        actual_output = list(flattened_result)
        self.assertEqual(actual_output, expected_output)


if __name__ == "__main__":
    unittest.main()
