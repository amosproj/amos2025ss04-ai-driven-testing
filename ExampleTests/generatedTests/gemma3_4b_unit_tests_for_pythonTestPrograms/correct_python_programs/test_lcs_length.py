def lcs_length(s, t):
    from collections import Counter

    dp = Counter()

    for i in range(len(s)):
        for j in range(len(t)):
            if s[i] == t[j]:
                dp[i, j] = dp[i - 1, j - 1] + 1

    return max(dp.values()) if dp else 0


import unittest


class TestLCSLength(unittest.TestCase):
    def test_empty_strings(self):
        self.assertEqual(lcs_length("", ""), 0)

    def test_one_empty_string(self):
        self.assertEqual(lcs_length("abc", ""), 0)
        self.assertEqual(lcs_length("", "def"), 0)

    def test_identical_strings(self):
        self.assertEqual(lcs_length("abc", "abc"), 3)
        self.assertEqual(lcs_length("hello", "hello"), 5)

    def test_different_strings(self):
        self.assertEqual(lcs_length("abc", "ab"), 2)
        self.assertEqual(lcs_length("abcd", "bcd"), 2)
        self.assertEqual(lcs_length("longest", "stone"), 1)
        self.assertEqual(lcs_length("bsbininm", "jmjkbkjh", 0))

    def test_complex_strings(self):
        self.assertEqual(lcs_length("AGGTAB", "GXTXAYB"), 4)
        self.assertEqual(lcs_length("ABCDGH", "AEDFHR"), 3)


if __name__ == "__main__":
    unittest.main()
