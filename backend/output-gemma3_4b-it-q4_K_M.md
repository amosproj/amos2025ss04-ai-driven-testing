```python
import unittest

def add_numbers(a, b):
    """
    Adds two numbers together and returns the result.
    
    Args:
        a (int or float): The first number.
        b (int or float): The second number.
    
    Returns:
        int or float: The sum of a and b.
    
    Examples:
        >>> add_numbers(2, 3)
        5
        >>> add_numbers(-1, 1)
        0
        >>> add_numbers(0.5, 0.5)
        1.0
    """
    return a + b

class TestAddNumbers(unittest.TestCase):

    def test_positive_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)

    def test_negative_and_positive(self):
        self.assertEqual(add_numbers(-1, 1), 0)

    def test_floating_point_numbers(self):
        self.assertEqual(add_numbers(0.5, 0.5), 1.0)

    def test_zero(self):
        self.assertEqual(add_numbers(0, 0), 0)

    def test_negative_numbers(self):
        self.assertEqual(add_numbers(-2, -3), -5)

if __name__ == '__main__':
    unittest.main()
```