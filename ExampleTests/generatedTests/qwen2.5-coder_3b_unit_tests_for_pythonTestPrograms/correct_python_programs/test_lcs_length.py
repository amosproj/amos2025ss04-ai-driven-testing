import unittest

class TestLcsLength(unittest.TestCase):
    def test_lcs_length(self):
        # Test cases for LCS length function
        self.assertEqual(lcs_length("abcde", "ace"), 3)
        self.assertEqual(lcs_length("abcdef", "bce"), 2)
        self.assertEqual(lcs_length("abcd", "efab"), 1)
        self.assertEqual(lcs_length("aaaa", "aa"), 2)
        self.assertEqual(lcs_length("", ""), 0)
        self.assertEqual(lcs_length("a", ""), 0)
        self.assertEqual(lcs_length("", "b"), 0)

if __name__ == '__main__':
    unittest.main()