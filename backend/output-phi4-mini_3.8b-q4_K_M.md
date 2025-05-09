```markdown
# Unit Tests for `add_numbers` Function

## Test Cases and Expected Results:

### Basic Addition:
- **Input:** `(2, 3)`
- **Expected Output:** `5`
  
### Adding Negative Numbers (Result is Zero):
- **Input:** `(-1, 1)`
- **Expected Output:** `0`

### Floating Point Number Addition:
- **Input:** `(0.5, 0.5)`
- **Expected Output:** `1.0`

## Unit Test Code:

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

    def test_addition(self):
        self.assertEqual(add_numbers(2, 3), 5)

    def test_negative_sum_zero(self):
        self.assertEqual(add_numbers(-1, 1), 0)

    def test_floating_point_number_adding(self):
        self.assertAlmostEqual(add_numbers(0.5, 0.5), 1.0)
    
if __name__ == '__main__':
    unittest.main()
```