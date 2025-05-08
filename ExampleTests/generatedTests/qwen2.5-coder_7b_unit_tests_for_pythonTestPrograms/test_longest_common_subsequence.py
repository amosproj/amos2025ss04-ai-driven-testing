import unittest


def longest_common_subsequence(a, b):
    if not a or not b:
        return ""

    elif a[0] == b[0]:
        return a[0] + longest_common_subsequence(a[1:], b[1:])

    else:
        return max(
            longest_common_subsequence(a, b[1:]),
            longest_common_subsequence(a[1:], b),
            key=len,
        )


class TestLongestCommonSubsequence(unittest.TestCase):
    def test_empty_strings(self):
        self.assertEqual(longest_common_subsequence("", ""), "")

    def test_one_empty_string(self):
        self.assertEqual(longest_common_subsequence("abc", ""), "")
        self.assertEqual(longest_common_subsequence("", "def"), "")

    def test_identical_strings(self):
        self.assertEqual(longest_common_subsequence("abc", "abc"), "abc")

    def test_no_common_chars(self):
        self.assertEqual(longest_common_subsequence("abc", "def"), "")

    def test_common_prefix_and_suffix(self):
        self.assertEqual(
            longest_common_subsequence("abcdefg", "zabcfgh"), "bcfg"
        )
        self.assertEqual(
            longest_common_subsequence("zabcfgh", "abcdefg"), "bcfg"
        )

    def test_common_mid_sequence(self):
        self.assertEqual(longest_common_subsequence("abcde", "xyzabxyz"), "ab")
        self.assertEqual(longest_common_subsequence("xyzabxyz", "abcde"), "ab")


if __name__ == "__main__":
    unittest.main()
