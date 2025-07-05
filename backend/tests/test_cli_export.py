#!/usr/bin/env python3
"""Test script for CLI export functionality."""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import cli  # noqa: E402


def test_cli_export():
    """Test the CLI export functionality."""
    print("=== Testing CLI Export Functionality ===")

    # Mock sys.argv to test different scenarios
    test_cases = [
        ["main.py", "--help"],
        ["main.py", "--export_format", "json"],
        ["main.py", "--export_all"],
        ["main.py", "--export_format", "markdown", "--export_all"],
        ["main.py", "--export_format", "invalid_format"],
    ]

    for i, test_args in enumerate(test_cases):
        print(f"\n--- Test Case {i+1}: {' '.join(test_args[1:])} ---")

        # Save original argv
        original_argv = sys.argv.copy()

        try:
            # Set test arguments
            sys.argv = test_args

            if "--help" in test_args:
                print("Help command - would show usage")
                continue

            # Parse arguments
            args = cli.parse_arguments()

            # Test validation
            print(
                f"Parsed export_format: {getattr(args, 'export_format', None)}"
            )
            print(f"Parsed export_all: {getattr(args, 'export_all', False)}")

            # Test validation function
            try:
                cli.validate_export_args(args)
                print("✅ Validation passed")
            except SystemExit as e:
                print(f"❌ Validation failed (exit code: {e.code})")

        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            # Restore original argv
            sys.argv = original_argv
            # Clear the cached args
            cli._parsed_args = None


def test_export_functionality():
    """Test the export functionality with sample content."""
    print("\n=== Testing Export Functionality ===")

    # Create a mock args object
    class MockArgs:
        def __init__(self, export_format=None, export_all=False):
            self.export_format = export_format
            self.export_all = export_all

    sample_content = """# Sample LLM Response

This is a test response from an LLM containing:

## Code Example
```python
def hello_world():
    return "Hello, World!"
```

## Test Cases
- Test valid input
- Test edge cases
- Test error handling
"""

    # Test export_all
    print("\n--- Testing export_all ---")
    args_all = MockArgs(export_all=True)
    try:
        cli.handle_export(args_all, sample_content, "test_output.md")
    except Exception as e:
        print(f"Error in export_all: {e}")

    # Test specific format
    print("\n--- Testing specific format (JSON) ---")
    args_json = MockArgs(export_format="json")
    try:
        cli.handle_export(args_json, sample_content, "test_output.md")
    except Exception as e:
        print(f"Error in JSON export: {e}")


if __name__ == "__main__":
    test_cli_export()
    test_export_functionality()
    print("\n=== CLI Export Test Complete ===")
