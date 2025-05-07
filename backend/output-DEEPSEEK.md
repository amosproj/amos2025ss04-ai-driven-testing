You can use Python's built-in `unittest` module to create unit tests for your function. Here is how you could write the test cases for this function:

```python
import unittest
from your_module import add_numbers  # adjust as necessary

class TestAddNumbers(unittest.TestCase):
    def setUp(self):
        pass  # if needed, use this method to set up any common variables or state for your tests
    
    def test_addition_of_positive_integers(self):
        self.assertEqual(add_numbers(2, 3), 5)
    
    def test_addition_of_negative_and_positive_integer(self):
        self.assertEqual(add_numbers(-1, 1), 0)
    
    def test_addition_of_floats(self):
        self.assertAlmostEqual(add_numbers(0.5, 0.5), 1.0)
        
if __name__ == '__main__':
    unittest.main()
```
You can save this code in a separate Python file (e.g., `test_add_numbers.py`). You could then run it from the command line with `python test_add_numbers.py` to execute your tests and see if they pass. 

Replace `your_module` with the name of your Python script where this function is defined. Make sure you import the correct module or replace these lines in the code as per your requirements.
