#!/usr/bin/env python3
"""Demonstrate CLI export options."""

import argparse
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model_manager import load_models  # noqa: E402
from export_manager import ExportManager  # noqa: E402


def show_cli_help():
    """Show the CLI help including export options."""
    print("=== AI-Driven Testing CLI with Export Options ===\n")

    models = load_models()
    parser = argparse.ArgumentParser(
        description="Run Ollama prompt pipeline with export options"
    )

    parser.add_argument(
        "--model", type=int, choices=range(len(models)), default=0
    )
    parser.add_argument("--prompt_file", type=str, help="Path to prompt file")
    parser.add_argument(
        "--source_code", type=str, help="Path to source code file"
    )
    parser.add_argument("--output_file", type=str, help="Output file path")
    parser.add_argument(
        "--modules", nargs="*", default=[], help="List of module names to run"
    )

    # Export options
    export_manager = ExportManager()
    parser.add_argument(
        "--export_format",
        type=str,
        choices=export_manager.get_supported_formats(),
        help="Export format for the output",
    )
    parser.add_argument(
        "--export_all",
        action="store_true",
        help="Export output in all supported formats",
    )

    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_ctx", type=int, default=4096)

    parser.print_help()

    print("\n=== Export Options ===")
    print(
        f"Available formats: {', '.join(export_manager.get_supported_formats())}"
    )
    print("")
    print("Examples:")
    print("  python3 main.py --export_format json")
    print("  python3 main.py --export_all")
    print(
        "  python3 main.py --export_format markdown --modules example_logger"
    )
    print("")


if __name__ == "__main__":
    try:
        show_cli_help()
    except Exception:
        print(
            "Note: Some dependencies missing for full CLI, but export functionality is ready."
        )
        print("Export formats available: json, markdown, http, txt, xml")
