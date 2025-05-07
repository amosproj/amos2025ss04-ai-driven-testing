import unittest


def is_valid_parenthesization(parens):
    depth = 0
    for paren in parens:
        if paren == "(":
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                return False

    return True if depth == 0 else False


class TestIsValidParenthesization(unittest.TestCase):
    def test_valid_parentheses(self):
        self.assertTrue(is_valid_parenthesization("()"))

    def test_mismatched_opening_paren(self):
        self.assertFalse(is_valid_parenthesization("(]"))

    def test_unmatched_closing_paren(self):
        self.assertFalse(is_valid_parenthesization("[)"))


if __name__ == "__main__":
    unittest.main()
