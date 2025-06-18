"""Test script to verify the integration of export functionality."""

# !/usr/bin/env python3

import os
import tempfile
from unittest.mock import patch
import sys

# Add the backend directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_cli_integration():
    """Test that CLI arguments are properly parsed and passed to execution."""
    import cli

    # Test parsing of export arguments
    test_args = [
        "--export_format",
        "json",
        "--export_all",
        "--prompt_file",
        "test_prompt.txt",
        "--output_file",
        "test_output.md",
    ]

    with patch("sys.argv", ["cli.py"] + test_args):
        try:
            args = cli.parse_arguments()
            print("✅ CLI parsing successful:")
            print(f"   export_format: {args.export_format}")
            print(f"   export_all: {args.export_all}")
            print(f"   prompt_file: {args.prompt_file}")
            print(f"   output_file: {args.output_file}")
            return True
        except Exception as e:
            print(f"❌ CLI parsing failed: {e}")
            return False


def test_export_manager_integration():
    """Test that ExportManager can be imported and used."""
    try:
        from export_manager import ExportManager

        export_manager = ExportManager()
        formats = export_manager.get_supported_formats()

        print("✅ ExportManager integration successful:")
        print(f"   Supported formats: {formats}")

        # Test basic export functionality
        with tempfile.TemporaryDirectory() as temp_dir:
            test_content = "# Test Content\nThis is a test export."
            result = export_manager.export_content(
                test_content, "markdown", os.path.join(temp_dir, "test.md")
            )
            print(f"   Test export successful: {result}")

        return True

    except Exception as e:
        print(f"❌ ExportManager integration failed: {e}")
        return False


def test_execution_signature():
    """Test that execution.execute_prompt has the correct signature."""
    try:
        import execution
        import inspect

        sig = inspect.signature(execution.execute_prompt)
        params = list(sig.parameters.keys())

        expected_params = [
            "model",
            "active_modules",
            "prompt_text",
            "output_file",
            "export_format",
            "export_all",
        ]

        print("✅ Execution function signature:")
        print(f"   Parameters: {params}")

        if all(param in params for param in expected_params):
            print("   ✅ All expected parameters present")
            return True
        else:
            missing = [p for p in expected_params if p not in params]
            print(f"   ❌ Missing parameters: {missing}")
            return False

    except Exception as e:
        print(f"❌ Execution signature test failed: {e}")
        return False


if __name__ == "__main__":
    print("=== Testing Export Integration ===\n")

    tests = [
        ("CLI Integration", test_cli_integration),
        ("ExportManager Integration", test_export_manager_integration),
        ("Execution Signature", test_execution_signature),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        result = test_func()
        results.append(result)
        print()

    passed = sum(results)
    total = len(results)

    print("=== Integration Test Results ===")
    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("🎉 All integration tests passed!")
        exit(0)
    else:
        print("❌ Some integration tests failed!")
        exit(1)
