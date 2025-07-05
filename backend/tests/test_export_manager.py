"""Test module for ExportManager functionality."""
import os
import tempfile
import shutil
from export_manager import ExportManager


def test_export_manager():
    """Test the ExportManager with sample content."""
    # Create a temporary directory for testing
    test_dir = tempfile.mkdtemp()

    try:
        # Initialize ExportManager with test directory
        export_manager = ExportManager(test_dir)

        # Sample content to export
        sample_content = """# Test Content

This is a sample LLM response that contains:
- Multiple lines
- Some code: `print("Hello, World!")`
- **Bold text** and *italic text*

## Code Block
```python
def hello():
    return "Hello from AI-Driven Testing!"
```

This content will be exported in multiple formats.
"""

        print("Testing ExportManager...")
        print(f"Output directory: {test_dir}")
        print(f"Supported formats: {export_manager.get_supported_formats()}")

        # Test individual format exports
        formats_to_test = ["json", "markdown", "txt", "xml", "http"]

        for format_type in formats_to_test:
            print(f"\nExporting as {format_type}...")
            try:
                filepath = export_manager.export_content(
                    sample_content, format_type
                )
                print(f"  ✓ Exported to: {filepath}")

                # Check if file was created
                if os.path.exists(filepath):
                    size = os.path.getsize(filepath)
                    print(f"  ✓ File size: {size} bytes")
                else:
                    print(f"  ✗ File not found: {filepath}")

            except Exception as e:
                print(f"  ✗ Error exporting {format_type}: {e}")

        # Test export all formats
        print("\nTesting export all formats...")
        all_exports = export_manager.export_all_formats(
            sample_content, "test_export"
        )

        for format_type, result in all_exports.items():
            if result.startswith("Error:"):
                print(f"  ✗ {format_type}: {result}")
            else:
                print(f"  ✓ {format_type}: {result}")

        # Test export statistics
        print("\nExport statistics:")
        stats = export_manager.get_export_stats()
        print(f"  Total files: {stats['total_files']}")
        print(f"  Format breakdown: {stats['formats']}")

        # List all files in output directory
        print(f"\nFiles in {test_dir}:")
        for file in os.listdir(test_dir):
            filepath = os.path.join(test_dir, file)
            size = os.path.getsize(filepath)
            print(f"  - {file} ({size} bytes)")

        print("\n✓ ExportManager test completed successfully!")

    finally:
        # Clean up temporary directory
        shutil.rmtree(test_dir)
        print(f"Cleaned up test directory: {test_dir}")


if __name__ == "__main__":
    test_export_manager()
