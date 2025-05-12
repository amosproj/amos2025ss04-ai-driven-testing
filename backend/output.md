To write unit tests for this function, you can use Python's built-in `unittest` module. Here are some examples of how to test different scenarios:

```python
import unittest
from your_module import add_numbers  # replace "your_module" with the name of the module where add_numbers function is defined

class TestAddNumbers(unittest.TestCase):
    def test_add_positive_integers(self):
        self.assertEqual(add_numbers(2, 3), 5)
    
    def test_add_negative_and_positive_integer(self):
        self.assertEqual(add_numbers(-1, 1), 0)
        
    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(0.5, 0.5), 1.0)

if __name__ == '__main__':
    unittest.main()
```
This code defines a class `TestAddNumbers` that inherits from `unittest.TestCase`. Each method in this class is a test case, which tests the add_numbers function with different inputs. 

The `assertEqual` and `assertAlmostEqual` methods are used to check if the output of the function matches the expected result. In these methods, you pass two arguments: the actual result returned by the function and the expected result. If they match, the test passes; otherwise, it fails. The `unittest.main()` call at the end runs all the tests.

You should replace "your_module" in the import statement with the name of your module where add_numbers is defined. You can run these tests using a command line interface by running `python -m unittest test_add_numbers` (where 'test_add_numbers' is the file name), or from within an IDE like PyCharm, if it supports unit testing.
