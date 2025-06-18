"""Export module for automatic LLM response export functionality."""

from modules.base import ModuleBase
from export_manager import ExportManager
import os


class ExportModule(ModuleBase):
    """Module that automatically exports LLM responses in multiple formats.

    This module demonstrates the export functionality integration.
    """

    def __init__(self):
        """Initialize the export module with ExportManager."""
        self.export_manager = ExportManager()

    def applies_before(self) -> bool:
        """Return False as this module only works after getting the response."""
        return False  # This module only works after getting the response

    def applies_after(self) -> bool:
        """Return True as this module processes responses."""
        return True

    def process_prompt(self, prompt: str) -> str:
        """Pass through the prompt unchanged."""
        return prompt

    def process_response(self, response: str, prompt: str) -> str:
        """Export the response in multiple formats automatically."""
        print("[ExportModule] Auto-exporting response in multiple formats...")

        # Create sample data structures
        response_data = {
            "response": response,
            "loading_time": 0.0,  # Not available in module context
            "final_time": 0.0,  # Not available in module context
        }

        prompt_data = {
            "model": {"id": "module_export", "name": "MODULE_EXPORT"},
            "prompt": prompt,
        }

        # Export in JSON and XML formats
        try:
            base_path = os.path.join(os.getcwd(), "module_export_output")

            # Export as JSON
            json_file = self.export_manager.export_output(
                response_data, prompt_data, base_path, "json"
            )
            print(f"[ExportModule] ✅ Exported JSON: {json_file}")

            # Export as XML
            xml_file = self.export_manager.export_output(
                response_data, prompt_data, base_path, "xml"
            )
            print(f"[ExportModule] ✅ Exported XML: {xml_file}")

        except Exception as e:
            print(f"[ExportModule] ❌ Export failed: {e}")

        return response
