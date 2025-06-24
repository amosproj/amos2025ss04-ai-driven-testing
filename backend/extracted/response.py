import sys
from pathlib import Path
sys.path.insert(0, '/code/extracted')
from prompt import *

import unittest
from math import *


class CalculatorTests(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(calculate_result(1, 2, "+"), 3)

    def test_subtraction(self):
        self.assertEqual(calculate_result(3, -2, "-"), 1)

    def test_multiplication(self):
        self.assertEqual(calculate_result(4, 6, "*"), 24)

    def test_division(self):
        with self.assertRaises(ValueError):
            calculate_result(5, 0, "/")


if __name__ == "__main__":
    unittest.main()