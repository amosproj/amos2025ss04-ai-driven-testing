import os
import argparse
from model_manager import load_models

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def parse_arguments():
    """Parse command-line arguments."""
    # Load allowed models for CLI choices
    loaded_models = load_models()

    parser = argparse.ArgumentParser(
        description="Run Ollama prompt sending script."
    )
    parser.add_argument(
        "--model", type=int, choices=range(len(loaded_models)), default=0
    )
    parser.add_argument(
        "--prompt_file",
        type=str,
        default=os.path.join(SCRIPT_DIR, "prompt.txt"),
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default=os.path.join(SCRIPT_DIR, "output.md"),
    )
    parser.add_argument(
        "--modules",
        nargs="*",
        default=[],
        help="List of modules to apply",
    )
    return parser.parse_args()
