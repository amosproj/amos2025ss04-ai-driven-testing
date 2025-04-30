def rpn_eval(tokens):
    def op(symbol, a, b):
        return {
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
            '*': lambda a, b: a * b,
            '/': lambda a, b: a / b
        }[symbol](b, a)

    stack = []

    for token in tokens:
        if isinstance(token, float):
            stack.append(token)
        else:
            a = stack.pop()
            b = stack.pop()
            stack.append(
                op(token, a, b)
            )

    return stack.pop()

import unittest

class TestRPNEval(unittest.TestCase):

    def test_basic_operations(self):
        tokens = [3.0, 4.0, '+', 2.0, '*']
        result = rpn_eval(tokens)
        self.assertEqual(result, 14)

    def test_subtraction_and_multiplication(self):
        tokens = [10.0, 5.0, '-', 1.0, 'x', 3]
        expected_result_stack_state = [
            {'-': lambda a: -a},
            {'*': lambda a, b: a * b}
        ]
        result_tokens = rpn_eval(tokens)
        self.assertEqual(result_tokens[-2], (expected_result_stack_state[1]['*'](tokens[-3], tokens[-4])))

    def test_division(self):
        tokens = [8.0, 4.0, '/']
        expected_value = 2
        result = rpn_eval(tokens)
        self.assertEqual(result, expected_value)

if __name__ == '__main__':
    unittest.main()