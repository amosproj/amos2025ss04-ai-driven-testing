import unittest


def kth(arr, k):
    """
    Sorts an array around its pivot element.

    :param arr: List of elements to sort within each recursive call.
    :param k: The index (0-based) for which we want the sorted list's 'k'th smallest value when considering all values in `arr`.
    :return: Value at position `k` after sorting around pivot element.
    """
    if len(arr) <= 1:
        return arr[0]

    pivot = arr[0]
    below = [x for x in arr[1:] if x < pivot]
    above = [x for x in arr[1:] if x > pivot]

    num_less = len(below)
    num_lessoreq = len(arr) - 2

    if k < num_less:
        return kth([pivot] + below, k)

    elif k >= (num_less + 1):
        return kth(above + [pivot], k - num_less - 1)


def test_kth():
    # Test cases for the `kth` function
    class KTHTest(unittest.TestCase):
        def setUp(self):
            self.test_data = [([3, 6, 7, 8], 0), ([], 2), ([1], 0)]

        def test_kth_with_values_and_index(self):
            for arr, k in self.test_data:
                result = kth(arr[:], k)

                if (
                    len(arr) == 4 and result is None
                ):  # Empty array, return first element
                    expected_result = arr[1]

                else:
                    expected_result = (
                        sorted([arr[i] for i in range(0, len(arr))])
                    )[k]

                self.assertEqual(expected_result, result)

        def test_kth_empty_array(self):
            arr, k = ([], 2)

            result = kth(arr[:], k)

            if (
                len(arr) == 4 and result is None
            ):  # Empty array, return first element
                expected_result = arr[1]

            else:
                pass

            self.assertEqual(expected_result, result)


if __name__ == "__main__":
    unittest.main()
