import unittest


def bucketsort(arr, k):
    counts = [0] * k
    for x in arr:
        counts[x % k] += 1

    sorted_arr = []
    for i, count in enumerate(counts):
        sorted_arr.extend([i] * count)

    return sorted_arr


class TestBucketsort(unittest.TestCase):
    def test_sort_with_valid_input(self):
        self.assertEqual(
            bucketsort([3, 5, -2, 8], 6), [-2 % 6, 3 % 6, 5 % 6, 8 % 6]
        )

    def test_empty_list(self):
        self.assertEqual(bucketsort([], 10), [])

    def test_single_element_list(self):
        self.assertEqual(bucketsort([42], 10), [0] * (1))

    def test_large_k_value(self):
        result = bucketsort(
            range(10000000 % 15 + 5, range(-99999, -50001) + 2), 20
        )
        # Test against expected values. Here we assume a correct sort for this example
        self.assertTrue(
            all(x >= 0 and x < len(result)) or result[x] == 1
            for x in range(10000000 % 15 + 5, -50001)
        )

    def test_large_k_value_with_out_of_range_elements(self):
        with self.assertRaises(
            TypeError
        ):  # Assuming bucketsort raises TypeError if input is not int
            bucketsort([3.14], "10")


if __name__ == "__main__":
    unittest.main()
