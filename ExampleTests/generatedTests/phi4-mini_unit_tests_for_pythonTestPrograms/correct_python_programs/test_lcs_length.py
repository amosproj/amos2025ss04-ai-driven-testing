import unittest
from collections import Counter


def lcs_length(s, t):
    dp = {}
    
    for i in range(len(s)):
        for j in range(len(t)):
            if s[i] == t[j]:
                dp[(i,j)] = 1 + (dp.get((i-1,j-1), 0) if (i > 0 and j > 0) else 0)
    
    return max(dp.values()) if dp else 0


class TestLCSLength(unittest.TestCase):

    def test_empty_strings(self):
        self.assertEqual(lcs_length("", ""), 0)

    def test_single_characters_same_string(self):
        self.assertEqual(lcs_length("a", "a"), 1)
        
    def test_different_strings_no_common_subsequence(self):
        self.assertEqual(lcs_length("abc", "def"), 0)

    def test_simple_case_with_overlap(self):
        s = 'AGGTAB'
        t = 'GXTXAYB'
        result = lcs_length(s, t)
        expected_result = max([x for x in Counter((s[i], s[j]) for i in range(len(s)) for j in range(i+1,len(s))).values() if (i,j) not equal to None and  [t[k] for k in range(t.index(s[i]), len(t)).index(s[j])] == 'X' + ('Y' if result > 0 else '')])
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()