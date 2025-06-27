import sys
from pathlib import Path
sys.path.insert(0, '/code/extracted')  # Add extracted dir to import path
from prompt import *  # Import functions from prompt.py
import unittest

class TestCalculateResult(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(calculate_result(2, 3, "+"), 5)

    def test_subtraction(self):
        self.assertEqual(calculate_result(10, 4, "-"), 6)

    def test_multiplication(self):
        self.assertEqual(calculate_result(3, 5, "*"), 15)

    def test_division(self):
        self.assertAlmostEqual(calculate_result(10, 2, "/"), 5.0)

    def test_division_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculate_result(5, 0, "/")

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            calculate_result(4, 2, "%")

if __name__ == "__main__":
    unittest.main()