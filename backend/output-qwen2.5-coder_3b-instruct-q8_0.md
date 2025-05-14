Here are some unit tests for the `add_numbers` function using Python's `unittest` framework:

```python
import unittest

class TestAddNumbers(unittest.TestCase):
    
    def test_add_two_positive_integers(self):
        self.assertEqual(add_numbers(2, 3), 5)
    
    def test_add_two_negative_integers(self):
        self.assertEqual(add_numbers(-1, 1), 0)
    
    def test_add_positive_and_negative_integer(self):
        self.assertEqual(add_numbers(2, -1), 1)
    
    def test_add_zero_and_non_zero_integer(self):
        self.assertEqual(add_numbers(0, 5), 5)
    
    def test_add_two_floats(self):
        self.assertAlmostEqual(add_numbers(0.5, 0.5), 1.0, places=2)
    
    def test_add_positive_and_negative_float(self):
        self.assertAlmostEqual(add_numbers(0.5, -0.5), 0.0, places=2)
    
    def test_add_zero_and_non_zero_float(self):
        self.assertAlmostEqual(add_numbers(0.0, 5.0), 5.0, places=2)

if __name__ == '__main__':
    unittest.main(argv=[''], exit=False)
```

### Explanation:
- **Test Cases**: Each test case checks a different scenario to ensure the function behaves as expected.
- **Assertions**:
  - `self.assertEqual`: Used for comparing two values that should be equal.
  - `self.assertAlmostEqual`: Used for comparing floating-point numbers with a specified number of decimal places, which is useful due to potential precision issues.
- **Running Tests**: The `unittest.main()` function is called at the end of the script to run all test cases.