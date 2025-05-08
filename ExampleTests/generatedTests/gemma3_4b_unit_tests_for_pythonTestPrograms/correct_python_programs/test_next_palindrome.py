def next_palindrome(digit_list):
    high_mid = len(digit_list) // 2
    low_mid = (len(digit_list) - 1) // 2
    while high_mid < len(digit_list) and low_mid >= 0:
        if digit_list[high_mid] == 9:
            digit_list[high_mid] = 0
            digit_list[low_mid] = 0
            high_mid += 1
            low_mid -= 1
        else:
            digit_list[high_mid] += 1
            if low_mid != high_mid:
                digit_list[low_mid] += 1
            return digit_list
    return [1] + (len(digit_list) - 1) * [0] + [1]


import unittest


class TestNextPalindrome(unittest.TestCase):
    def test_empty_list(self):
        self.assertEqual(next_palindrome([]), [1])

    def test_single_digit(self):
        self.assertEqual(next_palindrome([1]), [2])

    def test_simple_palindrome(self):
        self.assertEqual(next_palindrome([1, 2, 3, 2, 1]), [1, 2, 3, 2, 1])

    def test_increasing_number(self):
        self.assertEqual(next_palindrome([1, 2, 3, 4, 5]), [1, 2, 3, 4, 5])

    def test_number_with_9s(self):
        self.assertEqual(next_palindrome([1, 2, 9, 2, 1]), [1, 2, 3, 2, 1])

    def test_number_with_multiple_9s(self):
        self.assertEqual(next_palindrome([1, 2, 9, 9]), [1, 2, 3, 2, 1])

    def test_number_with_all_9s(self):
        self.assertEqual(next_palindrome([9, 9, 9]), [1, 0, 0, 1])

    def test_larger_number(self):
        self.assertEqual(next_palindrome([9, 9, 9, 9, 9]), [1, 0, 0, 0, 1])

    def test_another_number(self):
        self.assertEqual(next_palindrome([1, 2, 3, 4, 5, 6]), [1, 2, 3, 4, 5])

    def test_number_with_some_9s(self):
        self.assertEqual(
            next_palindrome([1, 2, 9, 9, 8, 9, 8, 9, 8, 9]),
            [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        )


if __name__ == "__main__":
    unittest.main()
