import unittest

class TestShuntingYard(unittest.TestCase):
    def test_shunting_yard(self):
        # Test case 1: Simple addition and subtraction
        self.assertEqual(shunting_yard(['3', '+', '4', '-', '2']), [3, 4, 2, '+', '-'])

        # Test case 2: Multiplication and division with precedence
        self.assertEqual(shunting_yard(['5', '*', '6', '/', '2']), [5, 6, 2, '*', '/'])

        # Test case 3: Simple sequence without operators
        self.assertEqual(shunting_yard([1, 2, 3]), [1, 2, 3])

        # Test case 4: Mixed operations with parentheses
        self.assertEqual(shunting_yard(['5', '+', '(', '6', '*', '2')]) + ')'], [5, 6, 2, '*', '+'])

        # Test case 5: Single operator with a number
        self.assertEqual(shunting_yard(['7', '+']), [7, '+'])

        # Test case 6: Empty list
        self.assertEqual(shunting_yard([]), [])

if __name__ == '__main__':
    unittest.main()