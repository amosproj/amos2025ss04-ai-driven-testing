import unittest
from collections import Counter

class LCSLengthTest(unittest.TestCase):
    def test_lcs_length(self):
        # Test case 1: Both strings are empty
        self.assertEqual(lcs_length("", ""), 0)
        
        # Test case 2: One string is "a", other is "b"
        self.assertEqual(lcs_length("a", "b"), 0)
        
        # Test case 3: s = "abc", t = "def" (no common characters)
        self.assertEqual(lcs_length("abc", "def"), 0)
        
        # Test case 4: s = "abcbdme", t = "abcdme" 
        # Expected LCS length should be 5 ('a','b','c','d','m')
        expected = 5
        result = lcs_length("abcbdme", "abcdme")
        self.assertEqual(result, expected)
        
        # Test case 5: s = "abcde", t = "ace"
        # Expected LCS length is 3 ('a','c','e')
        result = lcs_length("abcde", "ace")
        self.assertEqual(result, 3)

if __name__ == "__main__":
    unittest.main()