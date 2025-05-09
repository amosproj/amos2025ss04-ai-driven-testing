 To write unit tests for the `add_numbers` function, we can use Python's built-in unittest module. Here is an example of how the tests could be structured:

```python
import unittest

def add_numbers(a, b):
    # Your implementation here
    return a + b

class TestAddNumbers(unittest.TestCase):

    def test_add_integers(self):
        self.assertEqual(add_numbers(2, 3), 5)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(5, -3), 2)

    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(0.5, 0.5), 1.0)
        self.assertAlmostEqual(add_numbers(1.5, 2.3), 3.8)

if __name__ == "__main__":
    unittest.main()
```

In this example, the `TestAddNumbers` class contains two methods: `test_add_integers` and `test_add_floats`. Each method tests a specific case for the function, using the `assertEqual` and `assertAlmostEqual` functions to check the output of the `add_numbers` function against expected results.

The last line at the bottom ensures that the script runs the unit tests when it is executed directly. You can run these tests by executing the Python script from a command prompt or terminal, and they will print the results of each test case.