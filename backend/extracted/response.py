import sys
from pathlib import Path
sys.path.insert(0, '/code/extracted')  # Add extracted dir to import path
from prompt import *  # Import functions from prompt.py

import unittest


class CalculateResultTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_addition(self):
        self.assertEqual(calculate_result(1, 2, "+"), 3)

    def test_subtraction(self):
        self.assertEqual(calculate_result(1, -2, "-"), 1)

    def test_multiplication(self):
        self.assertEqual(calculate_result(5, 7, "*"), 35)

    def test_division(self):
        self.assertEqual(calculate_result(5, 0, "/"), 0)

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            calculate_result(1, "2", "-")
