def longest_common_subsequence(a, b):
    if not a or not b:
        return ''

    elif a[0] == b[0]:
        return a[0] + longest_common_subsequence(a[1:], b[1:])

    else:
        return max(
            longest_common_subsequence(a, b[1:]),
            longest_common_subsequence(a[1:], b),
            key=len
        )


import unittest

class TestLongestCommonSubsequence(unittest.TestCase):

    def test_empty_strings(self):
        self.assertEqual(longest_common_subsequence("", ""), "")

    def test_one_empty_string(self):
        self.assertEqual(longest_common_subsequence("abc", ""), "")
        self.assertEqual(longest_common_subsequence("", "abc"), "")

    def test_identical_strings(self):
        self.assertEqual(longest_common_subsequence("abc", "abc"), "abc")
        self.assertEqual(longest_common_subsequence("hello", "hello"), "hello")

    def test_different_strings(self):
        self.assertEqual(longest_common_subsequence("abc", "abd"), "")
        self.assertEqual(longest_common_subsequence("AGGTAB", "GXTXAYB"), "GTAB")
        self.assertEqual(longest_common_subsequence("ABCDGH", "AEDFGH"), "ADH")
        self.assertEqual(longest_common_subsequence("ABCBDAB", "BDCABA"), "BCAB")

    def test_longer_strings(self):
        self.assertEqual(longest_common_subsequence("thisisatest", "testing123"), "test")
        self.assertEqual(longest_common_subsequence("longestcommonsubsequence", "commonlongsubsequence"), "commonsubsequence")

    def test_overlapping_characters(self):
        self.assertEqual(longest_common_subsequence("aaaa", "aa"), "aa")
        self.assertEqual(longest_common_subsequence("abcabc", "abc"), "abc")

if __name__ == '__main__':
    unittest.main()