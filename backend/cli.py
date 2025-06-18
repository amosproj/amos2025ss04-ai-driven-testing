"""Command-line interface module for the AI-Driven Testing project."""
import os
import argparse
from model_manager import load_models
from schemas import PromptData, ModelMeta, InputData, InputOptions

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

_parsed_args = None  # Module-level cache


def parse_arguments() -> argparse.Namespace:
    global _parsed_args
    if _parsed_args is not None:
        return _parsed_args

    models = load_models()
    parser = argparse.ArgumentParser(description="Run Ollama prompt pipeline")

    parser.add_argument(
        "--model", type=int, choices=range(len(models)), default=0
    )
    parser.add_argument(
        "--prompt_file",
        type=str,
        default=os.path.join(SCRIPT_DIR, "user_message.txt"),
    )
    parser.add_argument(
        "--source_code",
        type=str,
        default=os.path.join(SCRIPT_DIR, "source_code.txt"),
    )
    parser.add_argument(
        "--output_file",
        type=str,
        default=os.path.join(SCRIPT_DIR, "output.md"),
    )
    parser.add_argument(
        "--modules", nargs="*", default=[], help="List of module names to run"
    )
    parser.add_argument(
        "--export_format",
        type=str,
        choices=["json", "markdown", "http", "txt", "xml"],
        default="markdown",
        help="Export format for the output (default: markdown)",
    )
    parser.add_argument(
        "--export_all",
        action="store_true",
        help="Export output in all supported formats",
    )
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_ctx", type=int, default=4096)

    return parser.parse_args()


def build_prompt_data(args: argparse.Namespace) -> PromptData:
    """Creates a PromptData object from CLI arguments."""
    models = load_models()
    model_info = models[args.model]

    # Load prompt text
    user_message = ""
    if args.prompt_file:
        with open(args.prompt_file, "r", encoding="utf-8") as f:
            user_message = f.read()

    # Load optional source code
    source_code = ""
    if args.source_code:
        with open(args.source_code, "r", encoding="utf-8") as f:
            source_code = f.read()

    return PromptData(
        model=ModelMeta(id=model["id"], name=model["name"]),
        input=InputData(
            user_message=user_message,
            source_code=source_code,
            system_message="You are a helpful assistant. Always respond in Markdown.",
            options=InputOptions(seed=args.seed, num_ctx=args.num_ctx),
        ),
        timeout=args.timeout,
    )
