"""
Code Coverage Analyzer Module.

This module analyzes code coverage for generated test code using coverage.py
or AST-based fallback analysis.
"""

import ast
import subprocess
import tempfile
from typing import Dict, List, Optional, Set
from pathlib import Path

from .base import ModuleBase
from schemas import PromptData, ResponseData


class CodeCoverageAnalyzer(ModuleBase):
    """
    Analyzes code coverage for generated test code.

    This module runs after the LLM generates test code and analyzes
    how much of the original source code is covered by the generated tests.
    """

    def __init__(self):
        """Initialize the CodeCoverageAnalyzer module."""
        self.coverage_available = self._check_coverage_availability()

    def applies_before(self) -> bool:
        """Return False as this module processes after LLM response."""
        """This module runs after response is received."""
        return False

    def applies_after(self) -> bool:
        """Return True as this module analyzes coverage after response."""
        """This module runs after response is received to analyze coverage."""
        return True

    def dependencies(self) -> List[type["ModuleBase"]]:
        """No dependencies for this module."""
        return []

    def _check_coverage_availability(self) -> bool:
        """
        Check if coverage.py is available in the system.

        Returns:
            True if coverage.py is available, False otherwise
        """
        try:
            # Try multiple Python executable names
            python_executables = [
                "python3",
                "python",
                "python3.11",
                "python3.10",
                "python3.9",
            ]

            for python_exe in python_executables:
                try:
                    result = subprocess.run(
                        [python_exe, "-m", "coverage", "--version"],
                        capture_output=True,
                        check=True,
                        text=True,
                        timeout=5,
                    )
                    if (
                        result.returncode == 0
                        and "coverage" in result.stdout.lower()
                    ):
                        return True
                except (
                    subprocess.CalledProcessError,
                    FileNotFoundError,
                    subprocess.TimeoutExpired,
                ):
                    continue

            # Also try importing coverage module directly
            try:
                import coverage  # noqa: F401

                return True
            except ImportError:
                pass

            return False

        except Exception:
            return False

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        """
        Analyze code coverage for the generated test code.

        Args:
            response_data: The response containing generated test code
            prompt_data: The original prompt containing source code

        Returns:
            ResponseData with coverage analysis added
        """
        # Only analyze if we have both source code and generated test code
        if not response_data.output.code or not prompt_data.input.source_code:
            return response_data

        # Analyze coverage
        coverage_data = self._analyze_coverage(
            source_code=prompt_data.input.source_code,
            test_code=response_data.output.code,
        )

        # Add coverage data to response
        response_data.output.coverage_data = coverage_data

        return response_data

    def _analyze_coverage(self, source_code: str, test_code: str) -> Dict:
        """
        Analyze code coverage using coverage.py or AST fallback.

        Args:
            source_code: The original source code to analyze
            test_code: The generated test code

        Returns:
            Dictionary containing coverage analysis results
        """
        if self.coverage_available:
            return self._analyze_with_coverage_py(source_code, test_code)
        else:
            return self._analyze_with_ast_fallback(source_code, test_code)

    def _analyze_with_coverage_py(
        self, source_code: str, test_code: str
    ) -> Dict:
        """
        Analyze coverage using coverage.py library.

        Args:
            source_code: The original source code
            test_code: The generated test code

        Returns:
            Coverage analysis results
        """
        try:
            # Find available Python executable
            python_exe = self._find_python_executable()
            if not python_exe:
                return self._create_error_result(
                    "No suitable Python executable found"
                )

            with tempfile.TemporaryDirectory() as temp_dir:
                # Create temporary files
                source_file = Path(temp_dir) / "source_code.py"
                test_file = Path(temp_dir) / "test_code.py"

                # Write source and test code to files
                source_file.write_text(source_code)
                # Ensure test code imports the source code
                test_content = f"from source_code import *\n{test_code}"
                test_file.write_text(test_content)

                # Run coverage analysis
                coverage_result = subprocess.run(
                    [
                        python_exe,
                        "-m",
                        "coverage",
                        "run",
                        "--source",
                        str(source_file.parent),
                        "--include",
                        "source_code.py",
                        str(test_file),
                    ],
                    capture_output=True,
                    text=True,
                    cwd=temp_dir,
                    timeout=30,
                )

                if coverage_result.returncode != 0:
                    return self._create_error_result(
                        f"Coverage execution failed: {coverage_result.stderr}"
                    )

                # Get coverage report
                report_result = subprocess.run(
                    [
                        python_exe,
                        "-m",
                        "coverage",
                        "report",
                        "--show-missing",
                        "--include",
                        "source_code.py",
                    ],
                    capture_output=True,
                    text=True,
                    cwd=temp_dir,
                    timeout=10,
                )

                if report_result.returncode != 0:
                    return self._create_error_result(
                        f"Coverage report failed: {report_result.stderr}"
                    )

                # Parse coverage report
                coverage_data = self._parse_coverage_report(
                    report_result.stdout
                )

                # Get detailed line information
                json_result = subprocess.run(
                    [
                        python_exe,
                        "-m",
                        "coverage",
                        "json",
                        "--include",
                        "source_code.py",
                    ],
                    capture_output=True,
                    text=True,
                    cwd=temp_dir,
                    timeout=10,
                )

                if json_result.returncode == 0:
                    try:
                        import json

                        json_data = json.loads(json_result.stdout)
                        if (
                            "files" in json_data
                            and "source_code.py" in json_data["files"]
                        ):
                            file_data = json_data["files"]["source_code.py"]
                            if "missing_lines" in file_data:
                                coverage_data["uncovered_lines"] = file_data[
                                    "missing_lines"
                                ]
                    except (json.JSONDecodeError, KeyError):
                        pass

                return coverage_data

        except subprocess.TimeoutExpired:
            return self._create_error_result("Coverage analysis timed out")
        except Exception as e:
            return self._create_error_result(
                f"Coverage analysis error: {str(e)}"
            )

    def _find_python_executable(self) -> Optional[str]:
        """
        Find a suitable Python executable for running coverage.py.

        Returns:
            Path to Python executable or None if not found
        """
        python_executables = [
            "python3",
            "python",
            "python3.11",
            "python3.10",
            "python3.9",
        ]

        for python_exe in python_executables:
            try:
                result = subprocess.run(
                    [python_exe, "-m", "coverage", "--version"],
                    capture_output=True,
                    check=True,
                    text=True,
                    timeout=5,
                )
                if result.returncode == 0:
                    return python_exe
            except (
                subprocess.CalledProcessError,
                FileNotFoundError,
                subprocess.TimeoutExpired,
            ):
                continue

        return None

    def _analyze_with_ast_fallback(
        self, source_code: str, test_code: str
    ) -> Dict:
        """
        Analyze coverage using AST-based fallback method.

        This method provides a heuristic-based coverage analysis when coverage.py
        is not available. It uses AST parsing to identify executable lines and
        estimates coverage based on function calls and variable references.

        Args:
            source_code: The original source code
            test_code: The generated test code

        Returns:
            Coverage analysis results with estimated coverage data
        """
        try:
            # Parse source code to get all executable lines and code structure
            source_lines = self._get_executable_lines(source_code)
            source_functions = self._extract_function_definitions(source_code)
            source_classes = self._extract_class_definitions(source_code)
            source_variables = self._extract_variable_definitions(source_code)

            # Parse test code to find function calls, variable references, and imports
            called_functions = self._extract_function_calls(test_code)
            referenced_variables = self._extract_variable_references(test_code)
            imported_names = self._extract_imports(test_code)

            # Enhanced heuristic: estimate covered lines based on multiple factors
            covered_lines = self._estimate_covered_lines_enhanced(
                source_code,
                source_functions,
                source_classes,
                source_variables,
                called_functions,
                referenced_variables,
                imported_names,
            )

            total_lines = len(source_lines)
            covered_count = len(covered_lines)
            uncovered_lines = list(source_lines - covered_lines)

            coverage_percentage = (
                (covered_count / total_lines * 100) if total_lines > 0 else 0
            )

            # Add branch coverage estimation
            branch_coverage = self._estimate_branch_coverage(
                source_code, called_functions, referenced_variables
            )

            return {
                "coverage_percentage": round(coverage_percentage, 2),
                "lines_covered": covered_count,
                "lines_total": total_lines,
                "uncovered_lines": sorted(uncovered_lines),
                "branch_coverage": round(branch_coverage, 2),
                "status": "estimated",
                "method": "ast_fallback_enhanced",
                "analysis_details": {
                    "functions_defined": len(source_functions),
                    "functions_called": len(
                        called_functions.intersection(source_functions)
                    ),
                    "classes_defined": len(source_classes),
                    "variables_defined": len(source_variables),
                    "variables_referenced": len(
                        referenced_variables.intersection(source_variables)
                    ),
                },
            }

        except Exception as e:
            return self._create_error_result(f"AST analysis error: {str(e)}")

    def _get_executable_lines(self, code: str) -> Set[int]:
        """
        Extract executable line numbers from source code using AST.

        Args:
            code: Source code to analyze

        Returns:
            Set of executable line numbers
        """
        try:
            tree = ast.parse(code)
            executable_lines = set()

            for node in ast.walk(tree):
                if hasattr(node, "lineno"):
                    # Consider these node types as executable
                    if isinstance(
                        node,
                        (
                            ast.FunctionDef,
                            ast.AsyncFunctionDef,
                            ast.ClassDef,
                            ast.Return,
                            ast.Assign,
                            ast.AnnAssign,
                            ast.AugAssign,
                            ast.Expr,
                            ast.If,
                            ast.For,
                            ast.While,
                            ast.With,
                            ast.Try,
                            ast.Assert,
                            ast.Raise,
                            ast.Import,
                            ast.ImportFrom,
                        ),
                    ):
                        executable_lines.add(node.lineno)

            return executable_lines

        except SyntaxError:
            # If parsing fails, estimate based on non-empty lines
            lines = code.split("\n")
            return {
                i + 1
                for i, line in enumerate(lines)
                if line.strip() and not line.strip().startswith("#")
            }

    def _extract_function_calls(self, test_code: str) -> Set[str]:
        """
        Extract function calls from test code using AST.

        Args:
            test_code: Test code to analyze

        Returns:
            Set of function names called in the test code
        """
        try:
            tree = ast.parse(test_code)
            function_calls = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        function_calls.add(node.func.id)
                    elif isinstance(node.func, ast.Attribute):
                        function_calls.add(node.func.attr)

            return function_calls

        except SyntaxError:
            # Simple fallback: extract identifiers from test code
            import re

            identifiers = re.findall(r"\b[a-zA-Z_][a-zA-Z0-9_]*\b", test_code)
            return set(identifiers)

    def _estimate_covered_lines(
        self, source_code: str, called_functions: Set[str]
    ) -> Set[int]:
        """
        Estimate which lines are covered based on function calls.

        Args:
            source_code: Original source code
            called_functions: Set of function names called in tests

        Returns:
            Set of estimated covered line numbers
        """
        try:
            tree = ast.parse(source_code)
            covered_lines = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    if node.name in called_functions:
                        # Add all lines in the function
                        for child in ast.walk(node):
                            if hasattr(child, "lineno"):
                                covered_lines.add(child.lineno)

                # Also add lines that contain called function names
                elif hasattr(node, "lineno"):
                    line_content = (
                        source_code.split("\n")[node.lineno - 1]
                        if node.lineno > 0
                        else ""
                    )
                    if any(func in line_content for func in called_functions):
                        covered_lines.add(node.lineno)

            return covered_lines

        except SyntaxError:
            return set()

    def _parse_coverage_report(self, report_output: str) -> Dict:
        """
        Parse coverage.py report output.

        Args:
            report_output: Coverage report text

        Returns:
            Parsed coverage data
        """
        try:
            lines = report_output.split("\n")
            coverage_data = {"method": "coverage.py", "status": "success"}

            # Look for coverage percentage in the report
            for line in lines:
                if "%" in line and "TOTAL" in line:
                    parts = line.split()
                    for part in parts:
                        if part.endswith("%"):
                            coverage_data["coverage_percentage"] = float(
                                part[:-1]
                            )
                            break

            # Extract line counts if available
            for line in lines:
                if "TOTAL" in line:
                    parts = line.split()
                    if len(parts) >= 4:
                        try:
                            coverage_data["lines_total"] = int(parts[1])
                            coverage_data["lines_covered"] = int(parts[2])
                        except (ValueError, IndexError):
                            pass

            return coverage_data

        except Exception as e:
            return self._create_error_result(f"Report parsing error: {str(e)}")

    def _create_error_result(self, error_message: str) -> Dict:
        """
        Create an error result dictionary.

        Args:
            error_message: Error description

        Returns:
            Error result dictionary
        """
        return {
            "error": error_message,
            "status": "error",
            "coverage_percentage": 0,
            "lines_covered": 0,
            "lines_total": 0,
            "uncovered_lines": [],
        }

    def _extract_function_definitions(self, source_code: str) -> Set[str]:
        """
        Extract function definition names from source code.

        Args:
            source_code: Source code to analyze

        Returns:
            Set of function names defined in the source code
        """
        try:
            tree = ast.parse(source_code)
            function_names = set()

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    function_names.add(node.name)

            return function_names

        except SyntaxError:
            return set()

    def _extract_class_definitions(self, source_code: str) -> Set[str]:
        """
        Extract class definition names from source code.

        Args:
            source_code: Source code to analyze

        Returns:
            Set of class names defined in the source code
        """
        try:
            tree = ast.parse(source_code)
            class_names = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef):
                    class_names.add(node.name)

            return class_names

        except SyntaxError:
            return set()

    def _extract_variable_definitions(self, source_code: str) -> Set[str]:
        """
        Extract variable definition names from source code.

        Args:
            source_code: Source code to analyze

        Returns:
            Set of variable names defined in the source code
        """
        try:
            tree = ast.parse(source_code)
            variable_names = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            variable_names.add(target.id)
                elif isinstance(node, ast.AnnAssign):
                    if isinstance(node.target, ast.Name):
                        variable_names.add(node.target.id)

            return variable_names

        except SyntaxError:
            return set()

    def _extract_variable_references(self, test_code: str) -> Set[str]:
        """
        Extract variable references from test code.

        Args:
            test_code: Test code to analyze

        Returns:
            Set of variable names referenced in the test code
        """
        try:
            tree = ast.parse(test_code)
            variable_references = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.Name) and isinstance(
                    node.ctx, ast.Load
                ):
                    variable_references.add(node.id)

            return variable_references

        except SyntaxError:
            return set()

    def _extract_imports(self, test_code: str) -> Set[str]:
        """
        Extract imported names from test code.

        Args:
            test_code: Test code to analyze

        Returns:
            Set of imported names
        """
        try:
            tree = ast.parse(test_code)
            imported_names = set()

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imported_names.add(
                            alias.asname if alias.asname else alias.name
                        )
                elif isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        imported_names.add(
                            alias.asname if alias.asname else alias.name
                        )

            return imported_names

        except SyntaxError:
            return set()

    def _estimate_covered_lines_enhanced(
        self,
        source_code: str,
        source_functions: Set[str],
        source_classes: Set[str],
        source_variables: Set[str],
        called_functions: Set[str],
        referenced_variables: Set[str],
        imported_names: Set[str],
    ) -> Set[int]:
        """
        Enhanced estimation of covered lines based on multiple factors.

        Args:
            source_code: Original source code
            source_functions: Set of function names defined in source
            source_classes: Set of class names defined in source
            source_variables: Set of variable names defined in source
            called_functions: Set of function names called in tests
            referenced_variables: Set of variable names referenced in tests
            imported_names: Set of imported names in tests

        Returns:
            Set of estimated covered line numbers
        """
        try:
            tree = ast.parse(source_code)
            covered_lines = set()

            # Track which functions/classes/variables are used
            used_functions = called_functions.intersection(source_functions)
            used_variables = referenced_variables.intersection(
                source_variables
            )
            used_imports = imported_names.intersection(
                source_functions.union(source_classes).union(source_variables)
            )

            for node in ast.walk(tree):
                if hasattr(node, "lineno"):
                    # Function definitions: mark as covered if function is called
                    if isinstance(
                        node, (ast.FunctionDef, ast.AsyncFunctionDef)
                    ):
                        if node.name in used_functions:
                            # Add all lines in the function
                            for child in ast.walk(node):
                                if hasattr(child, "lineno"):
                                    covered_lines.add(child.lineno)

                    # Class definitions: mark as covered if class is referenced
                    elif isinstance(node, ast.ClassDef):
                        if (
                            node.name in referenced_variables
                            or node.name in imported_names
                        ):
                            covered_lines.add(node.lineno)
                            # Add constructor and methods if they're called
                            for child in ast.walk(node):
                                if isinstance(
                                    child,
                                    (ast.FunctionDef, ast.AsyncFunctionDef),
                                ):
                                    if (
                                        child.name in used_functions
                                        or child.name == "__init__"
                                    ):
                                        for grandchild in ast.walk(child):
                                            if hasattr(grandchild, "lineno"):
                                                covered_lines.add(
                                                    grandchild.lineno
                                                )

                    # Variable assignments: mark as covered if variable is used
                    elif isinstance(node, (ast.Assign, ast.AnnAssign)):
                        line_has_used_variable = False
                        if isinstance(node, ast.Assign):
                            for target in node.targets:
                                if (
                                    isinstance(target, ast.Name)
                                    and target.id in used_variables
                                ):
                                    line_has_used_variable = True
                        elif isinstance(node, ast.AnnAssign):
                            if (
                                isinstance(node.target, ast.Name)
                                and node.target.id in used_variables
                            ):
                                line_has_used_variable = True

                        if line_has_used_variable:
                            covered_lines.add(node.lineno)

                    # Import statements: mark as covered if imported names are used
                    elif isinstance(node, (ast.Import, ast.ImportFrom)):
                        if any(
                            alias.name in used_imports
                            or (alias.asname and alias.asname in used_imports)
                            for alias in node.names
                        ):
                            covered_lines.add(node.lineno)

                    # Other executable statements: heuristic based on content
                    else:
                        line_content = (
                            source_code.split("\n")[node.lineno - 1]
                            if node.lineno > 0
                            else ""
                        )
                        if any(
                            func in line_content for func in used_functions
                        ) or any(
                            var in line_content for var in used_variables
                        ):
                            covered_lines.add(node.lineno)

            return covered_lines

        except SyntaxError:
            return set()

    def _estimate_branch_coverage(
        self,
        source_code: str,
        called_functions: Set[str],
        referenced_variables: Set[str],
    ) -> float:
        """
        Estimate branch coverage based on conditional statements.

        Args:
            source_code: Original source code
            called_functions: Set of function names called in tests
            referenced_variables: Set of variable names referenced in tests

        Returns:
            Estimated branch coverage percentage
        """
        try:
            tree = ast.parse(source_code)
            total_branches = 0
            covered_branches = 0

            for node in ast.walk(tree):
                # Count conditional branches
                if isinstance(node, (ast.If, ast.While, ast.For)):
                    total_branches += 1

                    # Simple heuristic: if the function containing this branch is called,
                    # assume some branch coverage
                    parent_function = self._find_parent_function(node, tree)
                    if (
                        parent_function
                        and parent_function.name in called_functions
                    ):
                        covered_branches += 0.5  # Assume partial coverage

                # Count exception handling branches
                elif isinstance(node, ast.Try):
                    total_branches += (
                        len(node.handlers)
                        + (1 if node.orelse else 0)
                        + (1 if node.finalbody else 0)
                    )
                    parent_function = self._find_parent_function(node, tree)
                    if (
                        parent_function
                        and parent_function.name in called_functions
                    ):
                        covered_branches += 0.3 * (
                            len(node.handlers)
                            + (1 if node.orelse else 0)
                            + (1 if node.finalbody else 0)
                        )

            return (
                (covered_branches / total_branches * 100)
                if total_branches > 0
                else 0
            )

        except SyntaxError:
            return 0

    def _find_parent_function(
        self, node: ast.AST, tree: ast.AST
    ) -> Optional[ast.FunctionDef]:
        """
        Find the parent function of a given AST node.

        Args:
            node: AST node to find parent for
            tree: Root AST tree

        Returns:
            Parent function node or None
        """
        for parent in ast.walk(tree):
            if isinstance(parent, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for child in ast.walk(parent):
                    if child is node:
                        return parent
        return None
