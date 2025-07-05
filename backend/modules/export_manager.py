"""Export Manager Module for AI-Driven Testing."""
import json
import os
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import Dict, Any, Optional

from modules.base import ModuleBase
from schemas import PromptData, ResponseData


class ExportManager(ModuleBase):
    """Module to export LLM responses in multiple formats with timestamped files."""

    def __init__(self, output_dir: str = "exports"):
        """Initialize ExportManager with output directory."""
        self.output_dir = output_dir
        self.supported_formats = ["json", "markdown", "http", "txt", "xml"]
        self._ensure_output_dir()

    def _ensure_output_dir(self):
        """Ensure the output directory exists."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _get_timestamp(self) -> str:
        """Generate timestamp for filename."""
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    def _get_filename(self, base_name: str, format_ext: str) -> str:
        """Generate timestamped filename."""
        timestamp = self._get_timestamp()
        return f"{base_name}_{timestamp}.{format_ext}"

    def applies_before(self) -> bool:
        """Export manager runs after response is received."""
        return False

    def applies_after(self) -> bool:
        """Export manager runs after response is received."""
        return True

    def dependencies(self) -> list[type["ModuleBase"]]:
        """No dependencies for export manager."""
        return []

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        """Process response and trigger export if configured."""
        # This will be called automatically by the module system
        # The actual export methods can be called directly by the API
        return response_data

    def export_as_json(
        self, content: str, filename: Optional[str] = None
    ) -> str:
        """Export content as JSON format."""
        if filename is None:
            filename = self._get_filename("export", "json")

        filepath = os.path.join(self.output_dir, filename)

        # Create structured JSON with metadata
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "format": "json",
            "content": content,
            "metadata": {
                "exported_by": "AI-Driven Testing ExportManager",
                "content_length": len(content),
            },
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        return filepath

    def export_as_markdown(
        self, content: str, filename: Optional[str] = None
    ) -> str:
        """Export content as Markdown format."""
        if filename is None:
            filename = self._get_filename("export", "md")

        filepath = os.path.join(self.output_dir, filename)

        # Add metadata header to markdown
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        markdown_content = f"""# AI-Driven Testing Export

**Exported:** {timestamp}
**Format:** Markdown
**Content Length:** {len(content)} characters

---

{content}
"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(markdown_content)

        return filepath

    def export_as_http(
        self, content: str, filename: Optional[str] = None
    ) -> str:
        """Export content as HTTP format (raw text + headers)."""
        if filename is None:
            filename = self._get_filename("export", "http")

        filepath = os.path.join(self.output_dir, filename)

        # Create HTTP-like format with headers
        timestamp = datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        http_content = f"""HTTP/1.1 200 OK
Content-Type: text/plain; charset=utf-8
Content-Length: {len(content)}
Date: {timestamp}
Server: AI-Driven Testing ExportManager
X-Export-Format: http

{content}
"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(http_content)

        return filepath

    def export_as_txt(
        self, content: str, filename: Optional[str] = None
    ) -> str:
        """Export content as plain text format."""
        if filename is None:
            filename = self._get_filename("export", "txt")

        filepath = os.path.join(self.output_dir, filename)

        # Add simple header to plain text
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        txt_content = f"""AI-Driven Testing Export
Exported: {timestamp}
Format: Plain Text
Content Length: {len(content)} characters

{'-' * 50}

{content}
"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(txt_content)

        return filepath

    def export_as_xml(
        self, content: str, filename: Optional[str] = None
    ) -> str:
        """Export content as XML format."""
        if filename is None:
            filename = self._get_filename("export", "xml")

        filepath = os.path.join(self.output_dir, filename)

        # Create XML structure
        root = ET.Element("export")

        # Add metadata
        metadata = ET.SubElement(root, "metadata")
        ET.SubElement(metadata, "timestamp").text = datetime.now().isoformat()
        ET.SubElement(metadata, "format").text = "xml"
        ET.SubElement(
            metadata, "exported_by"
        ).text = "AI-Driven Testing ExportManager"
        ET.SubElement(metadata, "content_length").text = str(len(content))

        # Add content
        content_elem = ET.SubElement(root, "content")
        content_elem.text = content

        # Write XML file
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ", level=0)
        tree.write(filepath, encoding="utf-8", xml_declaration=True)

        return filepath

    def export_content(
        self, content: str, format_type: str, filename: Optional[str] = None
    ) -> str:
        """Export content in the specified format."""
        if format_type not in self.supported_formats:
            raise ValueError(
                f"Unsupported format: {format_type}. Supported formats: {self.supported_formats}"
            )

        export_methods = {
            "json": self.export_as_json,
            "markdown": self.export_as_markdown,
            "http": self.export_as_http,
            "txt": self.export_as_txt,
            "xml": self.export_as_xml,
        }

        return export_methods[format_type](content, filename)

    def export_all_formats(
        self, content: str, base_filename: str = "export"
    ) -> Dict[str, str]:
        """Export content in all supported formats."""
        exported_files = {}

        for format_type in self.supported_formats:
            try:
                filepath = self.export_content(content, format_type, None)
                exported_files[format_type] = filepath
            except Exception as e:
                exported_files[format_type] = f"Error: {str(e)}"

        return exported_files

    def get_supported_formats(self) -> list[str]:
        """Return list of supported export formats."""
        return self.supported_formats.copy()

    def get_export_stats(self) -> Dict[str, Any]:
        """Get statistics about exported files."""
        if not os.path.exists(self.output_dir):
            return {"total_files": 0, "formats": {}}

        files = os.listdir(self.output_dir)
        format_counts = {}

        for file in files:
            if "." in file:
                ext = file.split(".")[-1]
                format_counts[ext] = format_counts.get(ext, 0) + 1

        return {
            "total_files": len(files),
            "formats": format_counts,
            "output_directory": self.output_dir,
        }


def get_module():
    """Factory function to create module instance."""
    return ExportManager()
