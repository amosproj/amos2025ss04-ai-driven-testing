"""Test execution utility for AI-generated unit tests.

This module provides functionality to run Python test scripts in a controlled
environment. It executes the generated test files as subprocesses, captures
their output, and determines success or failure based on the return code.
"""

import subprocess


def run_test_script(test_script_path):
    """Execute a Python test script and capture its output.

    Runs the specified test script as a subprocess with a timeout limit
    to prevent hanging. Captures both stdout and stderr for reporting.

    Args:
        test_script_path: Path to the Python test script to execute

    Returns:
        tuple: (success, output) where success is a boolean indicating if
               the test passed, and output contains the combined stdout and stderr
    """
    try:
        result = subprocess.run(
            ["python", str(test_script_path)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        success = result.returncode == 0
        output = result.stdout + "\n" + result.stderr
    except subprocess.TimeoutExpired:
        success = False
        output = "Test execution timed out."
    return success, output
