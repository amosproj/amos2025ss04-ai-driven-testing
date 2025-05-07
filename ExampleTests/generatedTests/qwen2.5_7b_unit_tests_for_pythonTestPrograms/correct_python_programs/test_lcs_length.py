def lcs_length(s, t):
    from collections import Counter

    dp = Counter()

    for i in range(len(s)):
        for j in range(len(t)):
            if s[i] == t[j]:
                dp[i, j] = dp[i - 1, j - 1] + 1

    return max(dp.values()) if dp else 0


import unittest
from collections import Counter


class TestLCSSolution(unittest.TestCase):
    def test_lcs_length(self):
        self.assertEqual(lcs_length("", ""), 0)
        self.assertEqual(lcs_length("a", "b"), 0)
        self.assertEqual(lcs_length("abcde", "ace"), 3)
        self.assertEqual(lcs_length("programming", "gaming"), 7)
        self.assertEqual(lcs_length("abcdabc", "abca"), 4)


if __name__ == "__main__":
    unittest.main()
