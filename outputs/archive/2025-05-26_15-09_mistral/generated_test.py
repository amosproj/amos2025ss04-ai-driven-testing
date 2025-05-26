import unittest

def add_numbers(a, b):
    """
    Adds two numbers together and returns the result.

    Args:
        a (int or float): The first number.
        b (int or float): The second number.

    Returns:
        int or float: The sum of a and b.
    """
    return a + b

class TestAddNumbers(unittest.TestCase):

    def test_add_integers(self):
        self.assertEqual(add_numbers(2, 3), 5)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(-2, 3), 1)
        self.assertEqual(add_numbers(9, -4), 5)

    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(0.5, 0.5), 1.0)
        self.assertAlmostEqual(add_numbers(1.23, -0.75), 0.48)
        self.assertAlmostEqual(add_numbers(-0.99, 1.1), 0.11)

if __name__ == "__main__":
    unittest.main()