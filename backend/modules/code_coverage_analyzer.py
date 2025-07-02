"""
Code Coverage Analyzer Module for AI-Driven Testing

This module provides code coverage analysis capabilities for generated test code.
It integrates with the AI testing system to measure how well generated tests
cover the source code.

Features:
- Coverage.py integration for accurate coverage measurement
- AST-based fallback analysis when coverage.py fails
- Support for various Python test frameworks
- Detailed coverage metrics and reporting
- Error handling for edge cases

Author: AI-Driven Testing Team
Version: 1.0.0
"""

import ast
import coverage
import tempfile
import os
import subprocess
import sys
from typing import Dict, List, Any
import json


class CodeCoverageAnalyzer:
    """
    Analyzes code coverage for generated test code.

    This module can run after test generation to measure how well the
    generated tests cover the original source code.
    """

    def __init__(self):
        """Initialize the Code Coverage Analyzer."""
        self.name = "code_coverage"
        self.description = "Analyzes code coverage of generated tests"

    def applies_before(self) -> bool:
        """
        Check if this module should run before test generation.

        Returns:
            bool: False, as coverage analysis runs after test generation
        """
        return False

    def applies_after(self) -> bool:
        """
        Check if this module should run after test generation.

        Returns:
            bool: True, as coverage analysis runs after test generation
        """
        return True

    def analyze_coverage(
        self, source_code: str, test_code: str
    ) -> Dict[str, Any]:
        """
        Analyze code coverage for the given source and test code.

        Args:
            source_code (str): The original source code to analyze
            test_code (str): The generated test code

        Returns:
            Dict[str, Any]: Coverage analysis results containing:
                - coverage_percentage: Overall coverage percentage
                - lines_covered: Number of lines covered by tests
                - lines_total: Total number of executable lines
                - branch_coverage: Branch coverage percentage (if available)
                - uncovered_lines: List of line numbers not covered
                - status: Analysis status ('success', 'error', 'fallback')
                - analysis_method: Method used ('coverage.py' or 'ast')
                - error: Error message if analysis failed
        """
        if not source_code.strip() or not test_code.strip():
            return {
                "status": "error",
                "error": "Source code and test code cannot be empty",
                "coverage_percentage": 0,
            }

        # Try coverage.py analysis first
        try:
            return self._analyze_with_coverage_py(source_code, test_code)
        except Exception as e:
            print(f"Coverage.py analysis failed: {e}")
            # Fallback to AST analysis
            try:
                return self._analyze_with_ast(source_code, test_code)
            except Exception as ast_e:
                return {
                    "status": "error",
                    "error": f"Both coverage.py and AST analysis failed. Coverage.py: {str(e)}, AST: {str(ast_e)}",
                    "coverage_percentage": 0,
                    "analysis_method": "failed",
                }

    def _analyze_with_coverage_py(
        self, source_code: str, test_code: str
    ) -> Dict[str, Any]:
        """
        Analyze coverage using the coverage.py library.

        Args:
            source_code (str): Source code to analyze
            test_code (str): Test code to run

        Returns:
            Dict[str, Any]: Coverage analysis results
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create source file
            source_file = os.path.join(temp_dir, "source_code.py")
            with open(source_file, "w", encoding="utf-8") as f:
                f.write(source_code)

            # Create test file that imports and uses the source code
            test_file = os.path.join(temp_dir, "test_code.py")
            test_content = self._prepare_test_code(source_code, test_code)
            with open(test_file, "w", encoding="utf-8") as f:
                f.write(test_content)

            # Initialize coverage
            cov = coverage.Coverage(
                source=[temp_dir],
                omit=[
                    test_file
                ],  # Don't measure coverage of the test file itself
            )

            try:
                # Start coverage measurement
                cov.start()

                # Execute the test code
                old_path = sys.path.copy()
                sys.path.insert(0, temp_dir)

                try:
                    # Import and run the test module
                    spec = __import__("test_code")

                    # If it's a unittest module, run it
                    if hasattr(spec, "unittest") or "unittest" in test_content:
                        subprocess.run(
                            [sys.executable, test_file],
                            cwd=temp_dir,
                            capture_output=True,
                            timeout=30,
                        )

                finally:
                    sys.path = old_path

                # Stop coverage measurement
                cov.stop()
                cov.save()

                # Generate coverage report
                covered_lines = []
                missing_lines = []
                total_lines = 0

                # Analyze the source file
                try:
                    analysis = cov._analyze(source_file)
                    total_lines = len(analysis.statements)
                    covered_lines = list(
                        analysis.statements - analysis.missing
                    )
                    missing_lines = list(analysis.missing)

                    coverage_percentage = (
                        (len(covered_lines) / total_lines * 100)
                        if total_lines > 0
                        else 0
                    )

                    return {
                        "status": "success",
                        "coverage_percentage": round(coverage_percentage, 2),
                        "lines_covered": len(covered_lines),
                        "lines_total": total_lines,
                        "uncovered_lines": missing_lines,
                        "analysis_method": "coverage.py",
                        "covered_lines": covered_lines,
                    }

                except Exception as analysis_error:
                    # If analysis fails, try to get basic metrics
                    return {
                        "status": "partial_success",
                        "coverage_percentage": 0,
                        "error": f"Coverage analysis incomplete: {str(analysis_error)}",
                        "analysis_method": "coverage.py",
                    }

            except Exception as exec_error:
                raise Exception(f"Test execution failed: {str(exec_error)}")

    def _prepare_test_code(self, source_code: str, test_code: str) -> str:
        """
        Prepare test code for execution with coverage measurement.

        Args:
            source_code (str): Original source code
            test_code (str): Test code to prepare

        Returns:
            str: Prepared test code that imports source functions
        """
        # Add the source code directly to the test file
        prepared_code = f"""
# Source code definitions
{source_code}

# Test code
{test_code}
"""

        return prepared_code

    def _analyze_with_ast(
        self, source_code: str, test_code: str
    ) -> Dict[str, Any]:
        """
        Analyze coverage using AST parsing as a fallback method.

        This method provides a basic coverage estimate by analyzing
        which functions/methods from the source code are referenced
        in the test code.

        Args:
            source_code (str): Source code to analyze
            test_code (str): Test code to analyze

        Returns:
            Dict[str, Any]: AST-based coverage analysis results
        """
        source_functions = self._extract_functions_ast(source_code)
        test_functions = self._extract_functions_ast(test_code)

        if not source_functions:
            return {
                "status": "error",
                "error": "No functions found in source code",
                "coverage_percentage": 0,
                "analysis_method": "ast",
            }

        # Count how many source functions are referenced in tests
        covered_functions = []
        for source_func in source_functions:
            if self._function_referenced_in_test(source_func, test_code):
                covered_functions.append(source_func)

        coverage_percentage = (
            (len(covered_functions) / len(source_functions) * 100)
            if source_functions
            else 0
        )

        return {
            "status": "success",
            "coverage_percentage": round(coverage_percentage, 2),
            "functions_in_source": len(source_functions),
            "functions_covered": len(covered_functions),
            "functions_in_tests": len(test_functions),
            "covered_functions": covered_functions,
            "uncovered_functions": [
                f for f in source_functions if f not in covered_functions
            ],
            "analysis_method": "ast",
            "note": "AST-based analysis provides function-level coverage estimation",
        }

    def _extract_functions_ast(self, code: str) -> List[str]:
        """
        Extract function and method names from code using AST.

        Args:
            code (str): Python code to analyze

        Returns:
            List[str]: List of function/method names found
        """
        try:
            tree = ast.parse(code)
            functions = []

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)
                elif isinstance(node, ast.AsyncFunctionDef):
                    functions.append(node.name)

            return functions
        except SyntaxError:
            return []
        except Exception:
            return []

    def _function_referenced_in_test(
        self, function_name: str, test_code: str
    ) -> bool:
        """
        Check if a function is referenced in the test code.

        Args:
            function_name (str): Name of the function to check
            test_code (str): Test code to search in

        Returns:
            bool: True if function is referenced, False otherwise
        """
        # Simple text-based check for function references
        # This could be enhanced with more sophisticated AST analysis
        return function_name in test_code and (
            f"{function_name}(" in test_code
            or f"self.{function_name}(" in test_code
        )

    def get_module_info(self) -> Dict[str, Any]:
        """
        Get information about this module.

        Returns:
            Dict[str, Any]: Module information
        """
        return {
            "name": self.name,
            "description": self.description,
            "version": "1.0.0",
            "applies_before": self.applies_before(),
            "applies_after": self.applies_after(),
            "capabilities": [
                "coverage.py integration",
                "AST-based analysis",
                "Function-level coverage",
                "Line-level coverage",
                "Error handling",
            ],
        }


# Module entry point for the module manager
def get_module():
    """
    Entry point for the module manager.

    Returns:
        CodeCoverageAnalyzer: Instance of the code coverage analyzer
    """
    return CodeCoverageAnalyzer()


# For standalone testing
if __name__ == "__main__":
    analyzer = CodeCoverageAnalyzer()

    # Example usage
    source = """
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b
"""

    test = """
import unittest

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

class TestMath(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)

if __name__ == '__main__':
    unittest.main()
"""

    result = analyzer.analyze_coverage(source, test)
    print("Coverage Analysis Result:")
    print(json.dumps(result, indent=2))
