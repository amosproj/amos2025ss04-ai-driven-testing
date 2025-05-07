To write unit tests for the `add_numbers` function in Python, you can use the `unittest` framework. Below is an example of how you can write test cases for this function:

```python
import unittest

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_integers(self):
        self.assertEqual(add_numbers(2, 3), 5)

    def test_add_negative_integers(self):
        self.assertEqual(add_numbers(-1, 1), 0)

    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(0.5, 0.5), 1.0, places=10)  # Use places to check precision

    def test_add_mixed_types(self):
        with self.assertRaises(TypeError):
            add_numbers("a", 3)

if __name__ == '__main__':
    unittest.main()
```

### Explanation:

1. **Importing `unittest`:** We start by importing the `unittest` module, which provides the necessary classes and functions to write unit tests.

2. **Creating a Test Class:** We define a class `TestAddNumbers` that inherits from `unittest.TestCase`. This class will contain all our test methods.

3. **Defining Test Methods:**
   - **`test_add_positive_integers`:** This test checks if the function correctly adds two positive integers.
   - **`test_add_negative_integers`:** This test checks if the function correctly handles negative integers.
   - **`test_add_floats`:** This test checks if the function correctly adds floating-point numbers, using `assertAlmostEqual` to account for potential precision issues.
   - **`test_add_mixed_types`:** This test ensures that the function raises a `TypeError` when passed mixed types.

4. **Running the Tests:** If you run this script, the `unittest.main()` function will automatically discover and execute all methods in the class that start with `test_`.

This setup will help ensure that the `add_numbers` function behaves as expected under various conditions.