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
        self.assertEqual(longest_common_subsequence('', ''), '')

    def test_single_character(self):
        self.assertEqual(longest_common_subsequence('a', 'b'), '')
        self.assertEqual(longest_common_subsequence('a', 'a'), 'a')

    def test_common_prefix(self):
        self.assertEqual(longest_common_subsequence('abcdef', 'abc'), 'abc')
        self.assertEqual(longest_common_subsequence('abcdef', 'xyzabc'), 'abc')

    def test_no_common_characters(self):
        self.assertEqual(longest_common_subsequence('abcdef', 'ghijkl'), '')

    def test_repeating_characters(self):
        self.assertEqual(longest_common_subsequence('aabbccdd', 'abbbcccd'), 'abbccd')
        self.assertEqual(longest_common_subsequence('aabbccdd', 'abcddd'), 'abcd')

if __name__ == '__main__':
    unittest.main()