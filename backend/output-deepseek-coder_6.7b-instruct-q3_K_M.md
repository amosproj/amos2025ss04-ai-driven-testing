Here is the unit test for the above Python function:

```python
import unittest
from your_module import add_numbers  # replace 'your_module' with the name of the module where this function resides.

class TestAddNumbers(unittest.TestCase):
    def setUp(self):
        pass  # if any setup is needed, define it here

    def test_add_positive_integers(self):
        self.assertEqual(add_numbers(2, 3), 5)

    def test_add_negative_and_positive_integer(self):
        self.assertEqual(add_numbers(-1, 1), 0)

    def test_add_floats(self):
        self.assertEqual(add_numbers(0.5, 0.5), 1.0)
        
if __name__ == '__main__':
    unittest.main()
```

In this unit test:
- We're using Python's built-in `unittest` module for creating tests and running them.
- The function `setUp(self)` in the TestCase class is a special method that runs before every test case, it can be used to set up any necessary conditions or data which will be common to all methods within this class (if you don't have an setup method then just delete/ignore it).
- The `test_add_positive_integers`, `test_add_negative_and_positive_integer` and `test_add_floats` are the test cases. Each of these methods tests a specific scenario using `assertEqual()` to check that the result is as expected. 

To run this unit test you can either copy it into your own script and run it directly or add it to an existing unittest suite. If you add it to an existing suite, remember to import all needed modules in the setUp method of TestCase class (like `your_module` in the example).
