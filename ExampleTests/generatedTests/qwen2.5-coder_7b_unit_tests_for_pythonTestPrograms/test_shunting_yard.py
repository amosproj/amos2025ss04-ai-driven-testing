import unittest

def shunting_yard(tokens):
    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2
    }

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

    def test_single_number(self):
        self.assertEqual(shunting_yard([5]), [5])

    def test_addition(self):
        self.assertEqual(shunting_yard([3, 2, '+']), [3, 2, '+'])

    def test_subtraction(self):
        self.assertEqual(shunting_yard([4, 1, '-']), [4, 1, '-'])

    def test_multiplication(self):
        self.assertEqual(shunting_yard([3, 4, '*']), [3, 4, '*'])

    def test_division(self):
        self.assertEqual(shunting_yard([8, 2, '/']), [8, 2, '/'])

    def test_multiple_operations(self):
        self.assertEqual(shunting_yard([5, 1, '+', 2, '*']), [5, 1, '+', 2, '*'])

    def test_precedence(self):
        self.assertEqual(shunting_yard([2, 3, '*', 4, '/']), [2, 3, '*', 4, '/'])

    def test_complex_expression(self):
        self.assertEqual(
            shunting_yard([10, 5, '+', 7, '*', 3, '-']),
            [10, 5, '+', 7, '*', 3, '-']
        )

if __name__ == '__main__':
    unittest.main()