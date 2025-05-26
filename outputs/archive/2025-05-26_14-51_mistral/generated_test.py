To write unit tests for the `add_numbers` function in Python using the built-in `unittest` module, you can create a new file named `test_add_numbers.py`. Here is an example of how the test suite could look:


import unittest
from your_module import add_numbers  # replace 'your_module' with the name of the module where add_numbers function resides

class TestAddNumbers(unittest.TestCase):
    def test_add_integers(self):
        self.assertEqual(add_numbers(2, 3), 5)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(0, 0), 0)
        self.assertEqual(add_numbers(-2, -3), -5)

    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(0.5, 0.5), 1.0)
        self.assertAlmostEqual(add_numbers(0.3, 0.7), 1.0)
        self.assertAlmostEqual(add_numbers(-0.2, 0.4), 0.2)

if __name__ == "__main__":
    unittest.main()