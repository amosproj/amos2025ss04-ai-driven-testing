 # Unit Tests for the `add_numbers` function

```python
import unittest
from your_module import add_numbers  # Assuming the function is in a module named 'your_module'

class TestAddNumbers(unittest.TestCase):

    def test_add_integers(self):
        self.assertEqual(add_numbers(2, 3), 5)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(0, 1), 1)
        self.assertEqual(add_numbers(-1, -1), 0)

    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(0.5, 0.5), 1.0)
        self.assertAlmostEqual(add_numbers(1.5, 2.5), 4.0)
        self.assertAlmostEqual(add_numbers(-0.5, -0.5), 0.0)

if __name__ == '__main__':
    unittest.main()
```

This unit test suite checks the `add_numbers` function for various cases of integer addition and floating-point number addition. The `unittest.TestCase.assertAlmostEqual()` function is used to handle floating-point numbers, which should be compared with a tolerance rather than exact equality due to rounding errors.