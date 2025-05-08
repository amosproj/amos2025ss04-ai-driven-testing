import unittest

from correct_python_programs.shunting_yardfromcorrect_python_programsfromcorrect_python_programs import \
    shunting_yard


class TestShuntingYard(unittest.TestCase):
    def test_shunting_yard(self):
        # Test case 1: Basic expression with multiple operators and parentheses
        tokens = [1, '+', 2, '-', 3]
        expected_output = [1, 2, 3, '-', '+']
        self.assertEqual(shunting_yard(tokens), expected_output)
        
    def test_shunting_yard_empty(self):
        # Test case 2: Empty token list
        tokens = []
        self.assertEqual(shunting_yard(tokens), [])

    def test_shunting_yard_single_number(self):
        # Test case 3: Single number in tokens list
        tokens = [5]
        expected_output = [5]
        self.assertEqual(shunting_yard(tokens), expected_output)
        
    def test_shunting_yard_single_operator(self):
        # Test case 4: Single operator with no numbers
        tokens = ['+']
        expected_output = []
        self.assertEqual(shunting_yard(tokens), expected_output)

    def test_shunting_yard_high_precedence_operator(self):
        # Test case 5: Operator with higher precedence than previous operators in stack
        tokens = [3, '+', 4, '*', 2]
        expected_output = [3,4,2,*,+]
        self.assertEqual(shunting_yard(tokens), expected_output)

    def test_shunting_yard_multiple_operators(self):
        # Test case 6: Multiple operators with different precedences
        tokens = ['*', '+', '-', 5, '/', 10]
        expected_output = [5,10,/,*,+,-]
        self.assertEqual(shunting_yard(tokens), expected_output)

if __name__ == '__main__':
    unittest.main()
```

This test class includes several test cases:
- Basic expression with multiple operators and parentheses
- Empty token list
- Single number in tokens list 
- Single operator with no numbers
- Operator with higher precedence than previous operators in stack
- Multiple operators with different precedences

The tests verify that the shunting_yard function correctly converts various token lists into postfix notation.

To run the tests, simply execute the script:
```bash
python -m unittest test_shunting_yard.py