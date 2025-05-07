import unittest


def shunting_yard(tokens):
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}

    rpntokens = []
    opstack = []
    for token in tokens:
        if isinstance(token, int):
            rpntokens.append(token)
        else:
            while opstack and precedence[token] <= precedence[opstack[-1]]:
                rpntokens.append(opstack.pop())
            opstack.append(token)

    while opstack:
        rpntokens.append(opstack.pop())

    return rpntokens


class TestShuntingYard(unittest.TestCase):
    def test_empty_input(self):
        self.assertEqual(shunting_yard([]), [])

    def test_simple_addition(self):
        tokens = [1, "+", 2]
        expected = [1, 2, "+"]
        self.assertEqual(shunting_yard(tokens), expected)

    def test_simple_multiplication(self):
        tokens = [1, "*", 2, "+", 3]
        expected = [1, 2, "*", 3, "+"]
        self.assertEqual(shunting_yard(tokens), expected)

    def test_complex_expression(self):
        tokens = [1, "+", 2, "*", 3, "+", 4, "*", 5]
        expected = [1, 2, "*", 3, "+", 4, "*", 5, "+"]
        self.assertEqual(shunting_yard(tokens), expected)

    def test_precedence_example(self):
        tokens = [1, "+", 2, "*", 3, "+", 4]
        expected = [1, 2, "*", 3, "+", 4, "+"]
        self.assertEqual(shunting_yard(tokens), expected)

    def test_division(self):
        tokens = [1, "/", 2, "+", 3]
        expected = [1, 2, "/", 3, "+"]
        self.assertEqual(shunting_yard(tokens), expected)

    def test_multiple_operators(self):
        tokens = [1, "+", 2, "*", 3, "/", 4, "+", 5, "-", 6]
        expected = [1, 2, "*", 3, "/", 4, "+", 5, "-", 6]
        self.assertEqual(shunting_yard(tokens), expected)


if __name__ == "__main__":
    unittest.main()
