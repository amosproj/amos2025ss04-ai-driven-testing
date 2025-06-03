import unittest
from your_module import (
    add_numbers,
)  # assuming the function is in a separate file named 'your_module.py'


class TestAddNumbers(unittest.TestCase):
    def test_add_integers(self):
        self.assertEqual(add_numbers(2, 3), 5)
        self.assertEqual(add_numbers(-1, 1), 0)
        self.assertEqual(add_numbers(0, 1), 1)
        self.assertEqual(add_numbers(-1, -1), 0)

    def test_add_floats(self):
        self.assertAlmostEqual(add_numbers(0.5, 0.5), 1.0)
        self.assertAlmostEqual(add_numbers(0.3, 0.7), 1.0)
        self.assertAlmostEqual(add_numbers(-0.2, 0.2), 0.0)


if __name__ == "__main__":
    unittest.main()
