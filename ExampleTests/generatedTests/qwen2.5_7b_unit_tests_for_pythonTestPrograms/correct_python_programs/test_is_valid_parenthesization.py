def is_valid_parenthesization(parens):
    depth = 0
    for paren in parens:
        if paren == "(":
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                return False

    return 0 == depth


import unittest


class TestIsValidParenthesization(unittest.TestCase):
    def test_empty_string(self):
        self.assertTrue(is_valid_parenthesization(""))

    def test_single_opening_parenthesis(self):
        self.assertFalse(is_valid_parenthesization("("))

    def test_single_closing_parenthesis(self):
        self.assertFalse(is_valid_parenthesization(")"))

    def test_balanced_parentheses(self):
        self.assertTrue(is_valid_parenthesization("()"))

    def test_unbalanced_opening_parentheses(self):
        self.assertFalse(is_valid_parenthesization("((("))

    def test_unbalanced_closing_parentheses(self):
        self.assertFalse(is_valid_parenthesization(")))"))

    def test_nested_balanced_parentheses(self):
        self.assertTrue(is_valid_parenthesization("(()())"))

    def test_mixed_parentheses(self):
        self.assertFalse(is_valid_parenthesization("())(("))


if __name__ == "__main__":
    unittest.main()
