import unittest

class TestLongestCommonSubsequence(unittest.TestCase):

    def test_longest_common_subsequence(self):
        # Test case 1: Both strings are identical
        self.assertEqual(longest_common_subsequence("abc", "abc"), "abc")
        
        # Test case 2: No common characters
        self.assertEqual(longest_common_subsequence("ab", "cd"), "")

        # Test case 3: Different lengths but same sequence
        self.assertEqual(longest_common_subsequence("abcd", "efgh"), "")

    def test_longest_common_subsequence(self):
        pass

if __name__ == '__main__':
    unittest.main()