import unittest

class TestIsValidParenthesization(unittest.TestCase):
    def test_valid_parentheses(self):
        self.assertTrue(is_valid_parenthesization("()"))

    def test_invalid_single_open_parenthesis(self):
        self.assertFalse(is_valid_parenthesization("("))

    def test_invalid_single_close_parenthesis(self):
        self.assertFalse(is_valid_parenthesization(")"))

    def test_invalid_multiple_unmatched_closing_parentheses(self):
        self.assertFalse(is_valid_parenthesization("(()))()"))

    def test_valid_multiple_matching_parentheses(self):
        self.assertTrue(is_valid_parenthesization("((()))"))

    def test_empty_string(self):
        self.assertTrue(is_valid_parenthesization(""))

if __name__ == '__main__':
    unittest.main()