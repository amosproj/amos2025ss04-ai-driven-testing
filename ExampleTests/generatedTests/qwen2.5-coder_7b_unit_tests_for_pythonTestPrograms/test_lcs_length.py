import unittest


def lcs_length(s, t):
    from collections import Counter

    dp = Counter()

    for i in range(len(s)):
        for j in range(len(t)):
            if s[i] == t[j]:
                dp[i, j] = dp[i - 1, j - 1] + 1

    return max(dp.values()) if dp else 0


class TestLCSLength(unittest.TestCase):
    def test_lcs_length_empty_strings(self):
        self.assertEqual(lcs_length("", ""), 0)

    def test_lcs_length_single_character_match(self):
        self.assertEqual(lcs_length("a", "a"), 1)
        self.assertEqual(lcs_length("b", "a"), 0)

    def test_lcs_length_multiple_characters_match(self):
        self.assertEqual(lcs_length("abcde", "ace"), 3)
        self.assertEqual(lcs_length("abcdefg", "xyzefgh"), 4)

    def test_lcs_length_no_match(self):
        self.assertEqual(lcs_length("abcde", "fghij"), 0)

    def test_lcs_length_one_string_empty(self):
        self.assertEqual(lcs_length("", "abcde"), 0)
        self.assertEqual(lcs_length("abcde", ""), 0)


if __name__ == "__main__":
    unittest.main()
