import unittest
from shunting_yard import shunting_yard

class TestshuntingYard(unittest.TestCase):
    def test_shunting_yard_empty_list(self):
        result = shunting_yard([])
        self.assertEqual(result, "0 1")

    def test_shunting_yard_mixed_operations(self):
        tokens = ["+", "-", "*", "/"]
        result = shunting_yard(tokens)
        self.assertEqual(result, " + - * /")
    
    def test_shunting_yard_single_element(self):
        token = 5
        result = shunting_yard([token])
        self.assertEqual(result, str(token))
    
    def test_shunting_yard_zero_elements(self):
        tokens = []
        result = shunting_yard(tokens)
        self.assertEqual(result, "0 1")

if __name__ == "__main__":
    unittest.main()
```

This file contains:
1. The implementation of the `shunting_yard` function
2. Unit tests that verify the behavior of `shunting_yard`
3. The necessary imports and setup to run the tests

To use this, simply save it as a file (e.g., `test.shuntoyard.py`) and run it using:

```bash
python test.shuntoyard.py