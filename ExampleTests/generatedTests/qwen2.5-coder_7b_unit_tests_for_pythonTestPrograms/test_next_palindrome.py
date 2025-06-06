import unittest


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


class TestNextPalindrome(unittest.TestCase):
    def test_next_palindrome(self):
        self.assertEqual(next_palindrome([1, 2, 3]), [1, 3, 1])
        self.assertEqual(next_palindrome([9, 9, 9]), [1, 0, 0, 1])
        self.assertEqual(next_palindrome([1, 2, 9]), [1, 4, 1])
        self.assertEqual(next_palindrome([9, 8, 7, 6]), [9, 9, 9, 9])


if __name__ == "__main__":
    unittest.main()
