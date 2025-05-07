import unittest


class TestIsValidParenthesization(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(is_valid_parenthesization(""), True)

    def test_single_pair(self):
        self.assertEqual(is_valid_parenthesization("()"), True)

    def test_more_pairs(self):
        self.assertEqual(is_valid_parenthesization("(())"), True)

    def test_incorrect_ending(self):
        self.assertEqual(is_valid_parenthesization("(()"), False)

    def test_starting_with_close(self):
        self.assertEqual(is_valid_parenthesization(")()"), False)


def is_valid_parenthesization(parens):
    depth = 0
    for paren in parens:
        if paren == "(":
            depth += 1
        else:
            depth -= 1
            if depth < 0:
                return False
    return depth == 0


if __name__ == "__main__":
    unittest.main()
