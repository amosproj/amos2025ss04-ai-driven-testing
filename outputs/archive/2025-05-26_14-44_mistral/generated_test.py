To write unit tests for the `add_numbers` function in Python, you can use the `unittest` library. Here is an example of how you might set up the tests:


import unittest

def add_numbers(a, b):
    """
    Adds two numbers together and returns the result.
    .... (same as original function documentation)
    """
    return a + b

class TestAddNumbers(unittest.TestCase):

    def test_add_ints(self):
        self.assertEqual(add_numbers(2, 3), 5)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(-5, 8), 3)

    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(0.5, 0.5), 1.0)
        self.assertAlmostEqual(add_numbers(1.25, -0.75), 0.5)
        self.assertAlmostEqual(add_numbers(-0.3, 0.2), 0.1)

if __name__ == "__main__":
    unittest.main()