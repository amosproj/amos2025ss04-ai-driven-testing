#!/usr/bin/env python3
"""Test suite for the Export Manager functionality.

Tests all export formats and validation of export features.
"""

import unittest
import tempfile
import os
import json
import xml.etree.ElementTree as ET
from export_manager import ExportManager


class TestExportManager(unittest.TestCase):
    """Test cases for ExportManager class."""

    def setUp(self):
        """Set up test fixtures."""
        self.export_manager = ExportManager()
        self.temp_dir = tempfile.mkdtemp()

        # Sample test data
        self.sample_response_data = {
            "response": "Here are unit tests for the add_numbers function:\n\n```python\nimport unittest\n\ndef test_add_numbers():\n    assert add_numbers(2, 3) == 5\n    assert add_numbers(-1, 1) == 0\n```",
            "loading_time": 2.5,
            "final_time": 5.0,
        }

        self.sample_prompt_data = {
            "model": {"id": "mistral:7b", "name": "MISTRAL"},
            "prompt": "Write unit tests for the add_numbers function:\n\ndef add_numbers(a, b):\n    return a + b",
        }

    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)

    def test_supported_formats(self):
        """Test that all expected formats are supported."""
        expected_formats = ["json", "markdown", "http", "txt", "xml"]
        self.assertEqual(
            self.export_manager.supported_formats, expected_formats
        )

    def test_json_export(self):
        """Test JSON export functionality."""
        output_path = os.path.join(self.temp_dir, "test_output")
        result_path = self.export_manager.export_output(
            self.sample_response_data,
            self.sample_prompt_data,
            output_path,
            "json",
        )

        # Verify file was created
        self.assertTrue(os.path.exists(result_path))
        self.assertTrue(result_path.endswith(".json"))

        # Verify JSON content
        with open(result_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.assertIn("metadata", data)
        self.assertIn("prompt", data)
        self.assertIn("response", data)
        self.assertEqual(data["metadata"]["model"]["id"], "mistral:7b")
        self.assertEqual(
            data["response"]["text"], self.sample_response_data["response"]
        )

    def test_markdown_export(self):
        """Test Markdown export functionality."""
        output_path = os.path.join(self.temp_dir, "test_output")
        result_path = self.export_manager.export_output(
            self.sample_response_data,
            self.sample_prompt_data,
            output_path,
            "markdown",
        )

        # Verify file was created
        self.assertTrue(os.path.exists(result_path))
        self.assertTrue(result_path.endswith(".markdown"))

        # Verify Markdown content
        with open(result_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("# AI-Driven Testing Output", content)
        self.assertIn("## Metadata", content)
        self.assertIn("## Prompt", content)
        self.assertIn("## Response", content)
        self.assertIn("MISTRAL", content)

    def test_xml_export(self):
        """Test XML export functionality."""
        output_path = os.path.join(self.temp_dir, "test_output")
        result_path = self.export_manager.export_output(
            self.sample_response_data,
            self.sample_prompt_data,
            output_path,
            "xml",
        )

        # Verify file was created
        self.assertTrue(os.path.exists(result_path))
        self.assertTrue(result_path.endswith(".xml"))

        # Verify XML is well-formed
        tree = ET.parse(result_path)
        root = tree.getroot()

        self.assertEqual(root.tag, "ai_testing_output")
        self.assertIsNotNone(root.find("metadata"))
        self.assertIsNotNone(root.find("prompt"))
        self.assertIsNotNone(root.find("response"))

    def test_http_export(self):
        """Test HTTP export functionality."""
        output_path = os.path.join(self.temp_dir, "test_output")
        result_path = self.export_manager.export_output(
            self.sample_response_data,
            self.sample_prompt_data,
            output_path,
            "http",
        )

        # Verify file was created
        self.assertTrue(os.path.exists(result_path))
        self.assertTrue(result_path.endswith(".http"))

        # Verify HTTP format
        with open(result_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("HTTP/1.1 200 OK", content)
        self.assertIn("Content-Type: application/json", content)
        self.assertIn("X-Model: mistral:7b", content)

    def test_txt_export(self):
        """Test plain text export functionality."""
        output_path = os.path.join(self.temp_dir, "test_output")
        result_path = self.export_manager.export_output(
            self.sample_response_data,
            self.sample_prompt_data,
            output_path,
            "txt",
        )

        # Verify file was created
        self.assertTrue(os.path.exists(result_path))
        self.assertTrue(result_path.endswith(".txt"))

        # Verify text content
        with open(result_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("AI-Driven Testing Output", content)
        self.assertIn("MISTRAL", content)
        self.assertIn("PROMPT", content)
        self.assertIn("RESPONSE", content)

    def test_multiple_formats_export(self):
        """Test exporting to multiple formats simultaneously."""
        output_path = os.path.join(self.temp_dir, "test_output")
        formats = ["json", "markdown", "xml"]

        result = self.export_manager.export_multiple_formats(
            self.sample_response_data,
            self.sample_prompt_data,
            output_path,
            formats,
        )

        # Verify all formats were exported
        self.assertEqual(len(result), 3)
        for fmt in formats:
            self.assertIn(fmt, result)
            self.assertIsNotNone(result[fmt])
            self.assertTrue(os.path.exists(result[fmt]))

    def test_unsupported_format(self):
        """Test handling of unsupported export format."""
        output_path = os.path.join(self.temp_dir, "test_output")

        with self.assertRaises(ValueError) as context:
            self.export_manager.export_output(
                self.sample_response_data,
                self.sample_prompt_data,
                output_path,
                "pdf",
            )

        self.assertIn("Unsupported format: pdf", str(context.exception))

    def test_create_export_data(self):
        """Test internal data structure creation."""
        export_data = self.export_manager._create_export_data(
            self.sample_response_data, self.sample_prompt_data
        )

        # Verify structure
        self.assertIn("metadata", export_data)
        self.assertIn("prompt", export_data)
        self.assertIn("response", export_data)

        # Verify metadata
        self.assertIn("timestamp", export_data["metadata"])
        self.assertIn("model", export_data["metadata"])
        self.assertIn("performance", export_data["metadata"])

        # Verify performance data
        self.assertEqual(
            export_data["metadata"]["performance"]["loading_time"], 2.5
        )
        self.assertEqual(
            export_data["metadata"]["performance"]["response_time"], 5.0
        )

        # Verify prompt and response data
        self.assertEqual(
            export_data["prompt"]["text"], self.sample_prompt_data["prompt"]
        )
        self.assertEqual(
            export_data["response"]["text"],
            self.sample_response_data["response"],
        )


if __name__ == "__main__":
    unittest.main()
