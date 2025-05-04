def is_valid_parenthesization(parens):
    depth = 0
    for paren in parens:
        if paren == '(':
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                return False

    return True if depth == 0 else False

import unittest

class TestIsValidParenthesization(unittest.TestCase):

    def test_empty_string(self):
        self.assertTrue(is_valid_parenthesization(""))

    def test_valid_parenthesization(self):
        self.assertTrue(is_valid_parenthesization("()"))
        self.assertTrue(is_valid_parenthesization("(()())"))
        self.assertTrue(is_valid_parenthesization("((()))"))

    def test_invalid_parenthesization(self):
        self.assertFalse(is_valid_parenthesization("("))
        self.assertFalse(is_valid_parenthesization(")"))
        self.assertFalse(is_valid_parenthesization("())"))
        self.assertFalse(is_valid_parenthesization("(()"))
        self.assertFalse(is_valid_parenthesization(")(()"))

    def test_complex_invalid(self):
        self.assertFalse(is_valid_parenthesization(")(()())"))
        self.assertFalse(is_valid_parenthesization("(()))("))

    def test_nested_valid(self):
        self.assertTrue(is_valid_parenthesization("((((()))))"))

    def test_multiple_pairs(self):
        self.assertTrue(is_valid_parenthesization("()()()"))

if __name__ == '__main__':
    unittest.main()