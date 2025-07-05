import sys
from pathlib import Path
sys.path.insert(0, '/code/extracted')  # Add extracted dir to import path
from prompt import *  # Import functions from prompt.py

import pytest  # required for pytest
import math  # required for math functions
from calculator import (
    calculator,
)  # import calculator module as defined earlier in this file


def test_addition():
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))
    result = calculator()
    assert result == (a + b)


def test_subtraction():
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))
    result = calculator()
    assert result == (a - b)


def test_multiplication():
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))
    result = calculator()
    assert result == (a * b)


def test_division():
    a = float(input("Enter first number: "))
    b = float(input("Enter second number: "))
    if b == 0:
        print("Error: Division by zero")
        return
    result = calculator()
    assert result == (a / b)


def test_invalid_operator():
    a = float(input("Enter first number: "))
    op = input("Enter operator (+, -, *, /): ")
    if op != "+":
        print("Invaliad operator")
        return
    result = calculator()
    assert result is None
