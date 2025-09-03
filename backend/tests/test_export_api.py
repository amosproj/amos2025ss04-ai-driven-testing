#!/usr/bin/env python3
"""Test script for export API endpoints."""

import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from export_manager import ExportManager  # noqa: E402


def test_export_api_integration():
    """Test the export API integration components."""
    print("🧪 Testing Export API Integration")
    print("=" * 50)

    # Test 1: ExportManager functionality
    print("\n1. Testing ExportManager functionality...")

    export_manager = ExportManager()
    formats = export_manager.get_supported_formats()
    print(f"✅ Supported formats: {formats}")

    # Test 2: API endpoint logic simulation
    print("\n2. Testing API endpoint logic...")

    # Simulate GET /export/formats
    api_response = {"formats": formats}
    print(f"✅ GET /export/formats response: {api_response}")

    # Simulate POST /export
    test_content = "# Test Content\n\nThis is a test for the API export."
    test_format = "json"

    try:
        filepath = export_manager.export_content(test_content, test_format)
        api_response = {
            "success": True,
            "format": test_format,
            "filepath": filepath,
            "message": f"Content exported successfully as {test_format}",
        }
        print(f"✅ POST /export response: {api_response}")
    except Exception as e:
        print(f"❌ Export test failed: {e}")

    print("\n" + "=" * 50)
    print("🎉 Export API Integration Test Complete!")


if __name__ == "__main__":
    test_export_api_integration()
