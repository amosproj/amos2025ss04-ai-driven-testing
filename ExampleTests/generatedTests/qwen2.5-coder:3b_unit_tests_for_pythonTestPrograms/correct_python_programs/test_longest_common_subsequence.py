import unittest

class TestLongestCommonSubsequence(unittest.TestCase):
    def test_empty_strings(self):
        self.assertEqual(longest_common_subsequence("", ""), "")

    def test_single_character(self):
        self.assertEqual(longest_common_subsequence("a", "a"), "a")
        self.assertEqual(longest_common_subsequence("a", "b"), "")
        self.assertEqual(longest_common_subsequence("b", "a"), "")

    def test_multiple_characters(self):
        self.assertEqual(longest_common_subsequence("abc", "def"), "")
        self.assertEqual(longest_common_subsequence("abcd", "abce"), "abc")
        self.assertEqual(longest_common_subsequence("abcdefg", "bcdefgh"), "bcdefg")

    def test_longer_strings(self):
        self.assertEqual(longest_common_subsequence("abcde", "ace"), "ace")
        self.assertEqual(longest_common_subsequence("abcdef", "bce"), "bc")

if __name__ == '__main__':
    unittest.main()