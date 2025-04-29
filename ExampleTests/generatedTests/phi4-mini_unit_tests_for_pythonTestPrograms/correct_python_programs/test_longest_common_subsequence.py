import unittest

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

class TestLongestCommonSubsequence(unittest.TestCase):

    def test_empty_strings(self):
        self.assertEqual(longest_common_subsequence('', ''), '')
    
    def test_single_character_longest_sequence(self):
        self.assertEqual(longest_common_subsequence('A', 'B'), '')  # No common character
        self.assertEqual(longest_common_subsequence('AA', 'BB'), 'AB' or 'BA')  # Both are equal in length

    def test_multiple_characters_with_common_sequence(self):
        self.assertEqual(longest_common_subsequence('ABCDEF', 'BCDEGHIJK'), 'BCD')

    def test_no_common_longest_characteristic(self):
        self.assertEqual(longest_common_subsequence('HELLO', 'WORLD'), '')  # No common characters

if __name__ == '__main__':
    unittest.main()