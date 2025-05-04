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
    def test_palindrome_123(self):
        input = [1, 2, 3]
        expected = [1, 3, 1]
        self.assertEqual(next_palindrome(input), expected)
    
    def test_palindrome_999(self):
        input = [9, 9, 9]
        expected = [1, 0, 0, 1]
        self.assertEqual(next_palindrome(input), expected)

    def test_palindrome_726(self):
        input = [7, 2, 6]
        expected = [7, 3, 7]
        self.assertEqual(next_palindrome(input), expected)
    
    def test_palindrome_987543210(self):
        input = [9,8,7,5,4,3,2,1,0]
        expected = [9,8,7,6,5,4,3,2,1,9]
        self.assertEqual(next_palindrome(input), expected)

    def test_smallest_palindrome(self):
        input = [1]
        expected = [2]
        self.assertEqual(next_palindrome(input), expected)
    
    def test_palindrome_908(self):
        input = [9, 0, 8]
        expected = [9, 1, 9]
        self.assertEqual(next_palindrome(input), expected)

if __name__ == '__main__':
    unittest.main()
```

This code includes:
- The original `next_palindrome` function
- A TestClass called `TestNextPalindrome`
- Multiple test cases with different input values and expected outputs
- Coverage of typical cases, edge cases (like 908), carry-over cases (like 999), and the smallest possible palindrome (1)
- The unittest framework to run all tests

To run the tests:
```bash
python -m unittest test_next_palindrome.py