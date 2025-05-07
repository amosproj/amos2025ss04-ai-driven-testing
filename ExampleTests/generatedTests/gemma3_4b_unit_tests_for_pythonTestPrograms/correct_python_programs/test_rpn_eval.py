import unittest
from io import StringIO


def rpn_eval(tokens):
    def op(symbol, a, b):
        return {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
        }[symbol](b, a)

    stack = []

    for token in tokens:
        if isinstance(token, float):
            stack.append(token)
        else:
            a = stack.pop()
            b = stack.pop()
            stack.append(op(token, a, b))

    return stack.pop()


class RpnEvalTest(unittest.TestCase):
    def test_empty_expression(self):
        self.assertRaises(IndexError, rpn_eval, [])

    def test_addition(self):
        tokens = [5.0, 3.0, "+"]
        self.assertEqual(rpn_eval(tokens), 8.0)

    def test_subtraction(self):
        tokens = [5.0, 3.0, "-"]
        self.assertEqual(rpn_eval(tokens), 2.0)

    def test_multiplication(self):
        tokens = [5.0, 3.0, "*"]
        self.assertEqual(rpn_eval(tokens), 15.0)

    def test_division(self):
        tokens = [10.0, 2.0, "/"]
        self.assertEqual(rpn_eval(tokens), 5.0)

    def test_complex_expression(self):
        tokens = [5.0, 3.0, 2.0, "+", "-", "*", 6.0, "/"]
        self.assertEqual(rpn_eval(tokens), 1.0)

    def test_different_data_types(self):
        tokens = [2.0, 3.0, "+", 4.0, "*"]
        self.assertEqual(rpn_eval(tokens), 14.0)


if __name__ == "__main__":
    unittest.main()
