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

import unittest
from collections import deque

class Stack:
    def __init__(self):
        self.items = deque()

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

class TestRPNEval(unittest.TestCase):

    def test_rpn_eval(self):
        self.assertAlmostEqual(rpn_eval([8.0, 2.0, '/']), 4.0)
        self.assertAlmostEqual(rpn_eval([3.0, 5.0, '+', 7.0, '*']), 48.0)
        self.assertAlmostEqual(rpn_eval([10.0, 2.0, '-', 3.0, '*', 9.0, '+']), 36.0)

    def test_rpn_eval_with_stack(self):
        stack = Stack()
        tokens = [8.0, 2.0, '/']
        for token in tokens:
            if isinstance(token, float):
                stack.push(token)
            else:
                b = stack.pop()
                a = stack.pop()
                stack.push(op(token, a, b))
        self.assertAlmostEqual(stack.pop(), 4.0)

if __name__ == '__main__':
    unittest.main()