import unittest


class TestNextPalindrome(unittest.TestCase):
    def test_next_palindrome(self):
        # Test case 1: Single digit
        self.assertEqual(next_palindrome([9]), [1])

        # Test case 2: Two digits with a carry
        self.assertEqual(next_palindrome([8, 9]), [9, 0])

        # Test case 3: Three digits with no carry
        self.assertEqual(next_palindrome([1, 2, 3]), [1, 2, 4])

        # Test case 4: Three digits with a carry
        self.assertEqual(next_palindrome([8, 9, 9]), [9, 0, 0])

        # Test case 5: Four digits with no carry
        self.assertEqual(next_palindrome([1, 2, 3, 4]), [1, 2, 4, 3])

        # Test case 6: Four digits with a carry
        self.assertEqual(next_palindrome([8, 9, 9, 9]), [9, 0, 0, 0])

        # Test case 7: Five digits with no carry
        self.assertEqual(next_palindrome([1, 2, 3, 4, 5]), [1, 2, 4, 3, 6])

        # Test case 8: Five digits with a carry
        self.assertEqual(next_palindrome([9, 9, 9, 9, 9]), [1, 0, 0, 0, 0])


if __name__ == "__main__":
    unittest.main()
