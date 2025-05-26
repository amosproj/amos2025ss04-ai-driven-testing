To write unit tests for the `add_numbers` function in Python, we can use the `unittest` module. Here is an example of how you could structure your test cases:


import unittest

def add_numbers(a, b):

class TestAddNumbers(unittest.TestCase):

    def test_add_integers(self):
        self.assertEqual(add_numbers(2, 3), 5)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(0, 1), 1)
        self.assertEqual(add_numbers(-2, -3), -5)

    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(0.5, 0.5), 1.0)
        self.assertAlmostEqual(add_numbers(0.25, 0.75), 1.0)
        self.assertAlmostEqual(add_numbers(-0.5, 0.5), 0.0)

if __name__ == '__main__':
    unittest.main()