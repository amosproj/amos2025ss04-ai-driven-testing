import unittest
from user_functions import calculate_sum, find_max


class TestUserFunctions(unittest.TestCase):
    def test_calculate_sum_empty_list(self):
        """Test calculate_sum with empty list"""
        result = calculate_sum([])
        self.assertEqual(result, 0)

    def test_calculate_sum_single_number(self):
        """Test calculate_sum with single number"""
        result = calculate_sum([5])
        self.assertEqual(result, 5)

    def test_calculate_sum_multiple_numbers(self):
        """Test calculate_sum with multiple numbers"""
        result = calculate_sum([1, 2, 3, 4, 5])
        self.assertEqual(result, 15)

    def test_calculate_sum_negative_numbers(self):
        """Test calculate_sum with negative numbers"""
        result = calculate_sum([-1, -2, -3])
        self.assertEqual(result, -6)

    def test_calculate_sum_mixed_numbers(self):
        """Test calculate_sum with positive and negative numbers"""
        result = calculate_sum([1, -2, 3, -4, 5])
        self.assertEqual(result, 3)

    def test_calculate_sum_floats(self):
        """Test calculate_sum with floating point numbers"""
        result = calculate_sum([1.5, 2.5, 3.0])
        self.assertEqual(result, 7.0)

    def test_find_max_empty_list(self):
        """Test find_max with empty list"""
        result = find_max([])
        self.assertIsNone(result)

    def test_find_max_single_number(self):
        """Test find_max with single number"""
        result = find_max([42])
        self.assertEqual(result, 42)

    def test_find_max_multiple_numbers(self):
        """Test find_max with multiple numbers"""
        result = find_max([1, 5, 3, 9, 2])
        self.assertEqual(result, 9)

    def test_find_max_negative_numbers(self):
        """Test find_max with negative numbers"""
        result = find_max([-5, -1, -10, -3])
        self.assertEqual(result, -1)

    def test_find_max_mixed_numbers(self):
        """Test find_max with positive and negative numbers"""
        result = find_max([-5, 10, -2, 8, 0])
        self.assertEqual(result, 10)

    def test_find_max_floats(self):
        """Test find_max with floating point numbers"""
        result = find_max([1.1, 3.7, 2.5, 3.6])
        self.assertEqual(result, 3.7)


if __name__ == "__main__":
    unittest.main()
