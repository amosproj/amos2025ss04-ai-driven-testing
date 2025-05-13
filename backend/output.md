 To write unit tests for the `add_numbers` function in Python, we can use the built-in `unittest` module. Here is an example of how you might structure the unit tests:

```python
import unittest

def add_numbers(a, b):
    # Your original implementation goes here...

class TestAddNumbers(unittest.TestCase):

    def test_add_integers(self):
        self.assertEqual(add_numbers(2, 3), 5)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(1, -1), 0)
        self.assertEqual(add_numbers(10, -4), 6)

    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(0.5, 0.5), 1.0)
        self.assertAlmostEqual(add_numbers(1.5, 2.3), 3.8)
        self.assertAlmostEqual(add_numbers(-0.3, 0.4), 0.1)

if __name__ == '__main__':
    unittest.main()
```

In the above code, we define a test case class `TestAddNumbers`, which inherits from `unittest.TestCase`. Inside this class, we create two methods: `test_add_integers` and `test_add_floats`. Each method contains multiple assertions that test different cases covered by the function's documentation examples.

Note that we use the `assertAlmostEqual` function to test our float addition case because float arithmetic is inherently inexact due to its representation as binary fractions. This function takes two arguments, the expected result and the actual result, and checks if they are close enough to be considered equal within a specified tolerance (by default, 0.01).

Finally, we call `unittest.main()` at the bottom to execute all the test cases defined in the `TestAddNumbers` class.