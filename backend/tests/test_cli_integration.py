#!/usr/bin/env python3
"""Test script to verify CLI export integration works correctly."""

import sys
import os
import tempfile
from unittest.mock import patch, MagicMock

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli import (  # noqa: E402
    parse_arguments,
    handle_export,
    validate_export_args,
)
from export_manager import ExportManager  # noqa: E402


def test_cli_export_integration():
    """Test the CLI export integration."""
    print("🧪 Testing CLI Export Integration")
    print("=" * 50)

    # Test 1: Validate export arguments
    print("\n1. Testing export argument validation...")

    # Mock sys.argv for testing
    test_args = [
        "main.py",
        "--export_format",
        "json",
        "--prompt_file",
        "test.txt",
        "--source_code",
        "test.py",
    ]

    with patch("sys.argv", test_args):
        try:
            args = parse_arguments()
            validate_export_args(args)
            print("✅ Export format validation passed")
        except SystemExit:
            print("❌ Export format validation failed")

    # Test 2: Test export_all flag
    print("\n2. Testing --export_all flag...")

    test_args_all = [
        "main.py",
        "--export_all",
        "--prompt_file",
        "test.txt",
        "--source_code",
        "test.py",
    ]

    with patch("sys.argv", test_args_all):
        try:
            args = parse_arguments()
            validate_export_args(args)
            print("✅ Export all flag validation passed")
        except SystemExit:
            print("❌ Export all flag validation failed")

    # Test 3: Test invalid format
    print("\n3. Testing invalid export format...")

    test_args_invalid = [
        "main.py",
        "--export_format",
        "invalid_format",
        "--prompt_file",
        "test.txt",
        "--source_code",
        "test.py",
    ]

    with patch("sys.argv", test_args_invalid):
        try:
            args = parse_arguments()
            validate_export_args(args)
            print("❌ Invalid format should have failed")
        except SystemExit:
            print("✅ Invalid format correctly rejected")

    # Test 4: Test handle_export function
    print("\n4. Testing handle_export function...")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Create mock args
        mock_args = MagicMock()
        mock_args.export_format = "json"
        mock_args.export_all = False

        # Test content
        test_content = "This is a test response from an LLM."
        output_file = os.path.join(temp_dir, "test_output.md")

        # Mock the ExportManager to use temp directory
        with patch("cli.ExportManager") as mock_export_manager:
            mock_manager = MagicMock()
            mock_manager.export_content.return_value = os.path.join(
                temp_dir, "test_export.json"
            )
            mock_manager.get_export_stats.return_value = {"total_files": 1}
            mock_export_manager.return_value = mock_manager

            # Test handle_export
            handle_export(mock_args, test_content, output_file)

            # Verify the export method was called
            mock_manager.export_content.assert_called_once_with(
                test_content, "json", None
            )
            print("✅ handle_export function works correctly")

    # Test 5: Test supported formats
    print("\n5. Testing supported formats...")

    export_manager = ExportManager()
    supported_formats = export_manager.get_supported_formats()
    expected_formats = ["json", "markdown", "http", "txt", "xml"]

    if set(supported_formats) == set(expected_formats):
        print(f"✅ All expected formats supported: {supported_formats}")
    else:
        print(
            f"❌ Format mismatch. Expected: {expected_formats}, Got: {supported_formats}"
        )

    print("\n" + "=" * 50)
    print("🎉 CLI Export Integration Test Complete!")


if __name__ == "__main__":
    test_cli_export_integration()
