#!/usr/bin/env python3
"""Demo script to showcase the export functionality."""

from export_manager import ExportManager
import os


def main():
    """Demonstrate the export functionality with sample data."""
    sample_response = """Here are unit tests for the add_numbers function:

```python
import unittest

class TestAddNumbers(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(add_numbers(2, 3), 5)

    def test_negative_numbers(self):
        self.assertEqual(add_numbers(-1, 1), 0)
if __name__ == '__main__':
    unittest.main()
```"""

    response_data = {
        "response": sample_response,
        "loading_time": 3.2,
        "final_time": 7.8,
    }

    prompt_data = {
        "model": {"id": "mistral:7b-instruct", "name": "MISTRAL"},
        "prompt": "Write unit tests for the add_numbers function",
    }

    export_manager = ExportManager()

    print("🚀 AI-Driven Testing Export Demo")
    print("=" * 50)

    exported_files = export_manager.export_multiple_formats(
        response_data, prompt_data, "demo_output"
    )

    print(f"\n✅ Successfully exported {len(exported_files)} files:")
    for fmt, path in exported_files.items():
        if path and os.path.exists(path):
            file_size = os.path.getsize(path)
            print(f"  - {fmt.upper()}: {path} ({file_size} bytes)")


if __name__ == "__main__":
    main()
