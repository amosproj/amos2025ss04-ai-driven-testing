import unittest

def rpn_eval(tokens):
    def op(symbol, a, b):
        return {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b
        }[symbol](a, b)

    stack = []

    for token in tokens:
        if isinstance(token, float):
            stack.append(token)
        else:
            a = stack.pop()
            b = stack.pop()
            stack.append(
                op(token, b, a)
            )

    return stack.pop()

class TestRPN(unittest.TestCase):

    def test_single_number(self):
        self.assertEqual(rpn_eval([3.0]), 3.0)

    def test_addition(self):
        self.assertEqual(rpn_eval([1.0, 2.0, '+']), 3.0)

    def test_subtraction(self):
        self.assertEqual(rpn_eval([5.0, 3.0, '-']), 2.0)

    def test_multiplication(self):
        self.assertEqual(rpn_eval([4.0, 3.0, '*']), 12.0)

    def test_division(self):
        self.assertEqual(rpn_eval([8.0, 4.0, '/']), 2.0)

    def test_complex_expression(self):
        self.assertEqual(rpn_eval([2.0, 3.0, '*', 5.0, '+', 1.0, '/']), 7.0)

if __name__ == '__main__':
    unittest.main()