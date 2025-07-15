import sys
from pathlib import Path
import unittest

sys.path.insert(0, "/code/extracted")  # Add extracted dir to import path
from prompt import (
    calculate_result,
    calculator,
)  # Import functions from prompt.py
import pytest  # required for pytest
import math  # required for math functions


class TestCalculateResult(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(calculate_result(2, 3, "+"), 5)

    def test_subtraction(self):
        self.assertEqual(calculate_result(5, 3, "-"), 2)

    def test_multiplication(self):
        self.assertEqual(calculate_result(4, 3, "*"), 12)

    def test_division(self):
        self.assertEqual(calculate_result(10, 2, "/"), 5.0)

    def test_division_by_zero(self):
        with self.assertRaises(ValueError):
            calculate_result(10, 0, "/")

    def test_invalid_operator(self):
        with self.assertRaises(ValueError):
            calculate_result(5, 3, "%")


def test_addition():
    """Test addition using pytest."""
    assert calculate_result(2, 3, "+") == 5


def test_subtraction():
    """Test subtraction using pytest."""
    assert calculate_result(5, 3, "-") == 2


def test_multiplication():
    """Test multiplication using pytest."""
    assert calculate_result(4, 3, "*") == 12


def test_division():
    """Test division using pytest."""
    assert calculate_result(10, 2, "/") == 5.0


def test_division_by_zero():
    """Test division by zero raises ValueError."""
    with pytest.raises(ValueError):
        calculate_result(10, 0, "/")


def test_invalid_operator():
    """Test invalid operator raises ValueError."""
    with pytest.raises(ValueError):
        calculate_result(5, 3, "%")


if __name__ == "__main__":
    unittest.main()
