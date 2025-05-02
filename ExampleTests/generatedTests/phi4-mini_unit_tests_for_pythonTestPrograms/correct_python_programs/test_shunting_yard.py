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
            while (opstack and precedence[token] <= precedence[opstack[-1]]):
                rpntokens.append(opstack.pop())
            opstack.append(token)

    while opstack:
        rpntokens.append(opstack.pop())

    return rpntokens


class TestShuntingYard(unittest.TestCase):

    def test_empty_input(self):
        self.assertEqual(shunting_yard([]), [])

    def test_single_number_token(self):
        tokens = [5]
        expected_output = [5]
        result = shunting_yard(tokens)
        for i in range(len(expected_output)):
            self.assertEqual(result[i], expected_output[i])

    def test_simple_expression_tokens(self):
        # Example: 1 + 2 * 3
        tokens = ['+', '2', '*', '3']
        expected_output = [2, '+', 3]
        result = shunting_yard(tokens)
        for i in range(len(expected_output)):
            self.assertEqual(result[i], expected_output[i])

    def test_precedence_tokens(self):
        # Example: (1 + 2) * 4
        tokens = ['+', '1', '2', '*', '4']
        expected_output = [3, '*', 4]
        result = shunting_yard(tokens)
        for i in range(len(expected_output)):
            self.assertEqual(result[i], expected_output[i])

    def test_mixed_tokens(self):
        # Example: (5 + ((1 * -2))) / (-6)
        tokens = ['(', '5', '+', '(', '*', '1', '-', '2', ')', '/', '-','6']
        expected_output = [(-3,), '/', 0]
        result = shunting_yard(tokens)
        for i in range(len(expected_output)):
            self.assertEqual(result[i], expected_output[i])

if __name__ == '__main__':
    unittest.main()