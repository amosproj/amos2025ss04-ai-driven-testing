import unittest


def max_sublist_sum(arr):
    max_ending_here = 0
    max_so_far = 0

    for x in arr:
        max_ending_here = max(max_ending_here + x, 0)
        max_so_far = max(max_so_far, max_ending_here)

    return max_so_far


class TestMaxSublistSum(unittest.TestCase):

    def test_empty_list(self):
        self.assertEqual(max_sublist_sum([]), 0)

    def test_single_element_non_negative(self):
        self.assertEqual(max_sublist_sum([5]), 5)
    
    def test_single_element_negative_one(self):
        self.assertEqual(max_sublist_sum([-1]), -1)

    def test_positive_numbers_all(self):
        arr = [2, 3, -7, 4, 8]
        expected_result = max(arr) + min([x for x in arr if x > 0])
        result = max_sublist_sum(arr)
        self.assertEqual(result, expected_result)

    def test_negative_numbers_all(self):
        arr = [-2, -3, -7, -4, -8]
        assert_equal(max_sublist_sum(arr), min(arr))
    
    def test_mixed_positive_and_negative_numbers(self):
        arr = [1, 0, -5, 10, 15]
        expected_result = max([x for x in arr if x > 0]) + abs(min(x for x in arr if x < 0)) 
        result = max_sublist_sum(arr)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()