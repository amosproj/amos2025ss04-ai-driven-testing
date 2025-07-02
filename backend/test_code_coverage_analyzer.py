"""Unit tests for the Code Coverage Analyzer module."""

import pytest
import tempfile
import os
from modules.code_coverage_analyzer import CodeCoverageAnalyzer


class TestCodeCoverageAnalyzer:
    """Test cases for CodeCoverageAnalyzer."""

    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = CodeCoverageAnalyzer()

    def test_analyzer_initialization(self):
        """Test that the analyzer initializes correctly."""
        assert self.analyzer is not None
        assert hasattr(self.analyzer, 'analyze_coverage')
        assert hasattr(self.analyzer, 'applies_before')
        assert hasattr(self.analyzer, 'applies_after')

    def test_applies_before(self):
        """Test applies_before method."""
        result = self.analyzer.applies_before()
        assert isinstance(result, bool)
        assert result is False  # Code coverage is typically run after

    def test_applies_after(self):
        """Test applies_after method."""
        result = self.analyzer.applies_after()
        assert isinstance(result, bool)
        assert result is True  # Code coverage is run after generation

    def test_analyze_coverage_simple(self):
        """Test coverage analysis with simple code."""
        source_code = """
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
"""

        test_code = """
import unittest

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
    
    def test_multiply(self):
        self.assertEqual(multiply(3, 4), 12)
        self.assertEqual(multiply(-2, 5), -10)

if __name__ == '__main__':
    unittest.main()
"""

        result = self.analyzer.analyze_coverage(source_code, test_code)
        
        assert isinstance(result, dict)
        assert 'coverage_percentage' in result
        assert 'status' in result
        assert result['status'] == 'success'
        assert isinstance(result['coverage_percentage'], (int, float))

    def test_analyze_coverage_with_invalid_test(self):
        """Test coverage analysis with invalid test code."""
        source_code = "def hello(): return 'world'"
        test_code = "this is not valid python code"
        
        result = self.analyzer.analyze_coverage(source_code, test_code)
        
        assert isinstance(result, dict)
        assert 'error' in result or 'status' in result

    def test_analyze_coverage_with_empty_code(self):
        """Test coverage analysis with empty code."""
        result = self.analyzer.analyze_coverage("", "")
        
        assert isinstance(result, dict)
        assert 'error' in result or 'status' in result

    def test_analyze_coverage_ast_fallback(self):
        """Test AST analysis fallback when coverage.py fails."""
        source_code = """
def function_one():
    return "one"

def function_two():
    return "two"

class TestClass:
    def method_one(self):
        return "method one"
"""

        test_code = """
# This test doesn't actually test anything meaningful
# but should trigger AST analysis
def function_one():
    return "one"

print("Test executed")
"""
        
        result = self.analyzer.analyze_coverage(source_code, test_code)
        
        assert isinstance(result, dict)
        assert 'status' in result

    def test_extract_functions_ast(self):
        """Test AST function extraction."""
        source_code = """
def func1():
    pass

def func2(arg):
    return arg

class MyClass:
    def method1(self):
        return "test"
    
    def method2(self, x, y):
        return x + y
"""
        
        # This tests internal AST functionality
        functions = self.analyzer._extract_functions_ast(source_code)
        assert isinstance(functions, list)
        # Should find functions and methods
        assert len(functions) >= 2  # At least func1, func2

    def test_extract_functions_ast_invalid(self):
        """Test AST function extraction with invalid code."""
        invalid_code = "def invalid_syntax( this is not python"
        
        functions = self.analyzer._extract_functions_ast(invalid_code)
        assert isinstance(functions, list)
        assert len(functions) == 0  # Should return empty list for invalid code
