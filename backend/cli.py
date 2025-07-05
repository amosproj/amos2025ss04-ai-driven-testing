"""Command-line interface module for AI-Driven Testing with export support."""
import os
import argparse
from model_manager import load_models
from schemas import PromptData, ModelMeta, InputData, InputOptions
from export_manager import ExportManager

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

_parsed_args = None  # Module-level cache


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments including export options."""
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
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num_ctx", type=int, default=4096)

    # Export options
    export_manager = ExportManager()
    parser.add_argument(
        "--export_format",
        type=str,
        choices=export_manager.get_supported_formats(),
        help="Export format for the output (default: markdown)",
    )
    parser.add_argument(
        "--export_all",
        action="store_true",
        help="Export output in all supported formats",
    )

    parser.add_argument(
        "--command-order",
        dest="order",
        action="store_true",  # Changed from store_false
        help="Set module ordering to true if this tag is used",
    )

    parser.add_argument("--timeout", type=int)
    parser.add_argument(
        "--use-links",
        nargs="+",
        type=str,
        help="Provide one or more web links to include in the context",
    )

    _parsed_args = parser.parse_args()
    return _parsed_args


def build_prompt_data(args: argparse.Namespace, model) -> PromptData:
    """Create a PromptData object from CLI arguments."""
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


def handle_export(
    args: argparse.Namespace, response_content: str, output_file: str
) -> None:
    """Handle export functionality based on CLI arguments."""
    if not args.export_format and not args.export_all:
        return  # No export requested

    try:
        export_manager = ExportManager("./exports")

        if args.export_all:
            print("📤 Exporting response in all formats...")
            exported_files = export_manager.export_all_formats(
                response_content, "cli_export"
            )

            print("✅ Export completed:")
            for format_type, filepath in exported_files.items():
                if filepath.startswith("Error:"):
                    print(f"  ❌ {format_type.upper()}: {filepath}")
                else:
                    print(f"  ✅ {format_type.upper()}: {filepath}")

        elif args.export_format:
            print(f"📤 Exporting response as {args.export_format.upper()}...")

            filepath = export_manager.export_content(
                response_content,
                args.export_format,
                None,  # Let it generate timestamped filename
            )
            print(f"✅ Exported to: {filepath}")

        # Show export statistics
        stats = export_manager.get_export_stats()
        print(f"📊 Total exported files: {stats['total_files']}")

    except Exception as e:
        print(f"❌ Export failed: {e}")


def validate_export_args(args: argparse.Namespace) -> None:
    """Validate export arguments and show helpful messages."""
    if args.export_format and args.export_all:
        print(
            "⚠️  Warning: Both --export_format and --export_all specified. Using --export_all."
        )
        args.export_format = None  # Clear specific format when exporting all

    if args.export_format or args.export_all:
        export_manager = ExportManager()
        supported_formats = export_manager.get_supported_formats()

        if args.export_format and args.export_format not in supported_formats:
            print(f"❌ Error: Unsupported export format '{args.export_format}'")
            print(f"📋 Supported formats: {', '.join(supported_formats)}")
            exit(1)

        print(f"📋 Available export formats: {', '.join(supported_formats)}")

        if args.export_all:
            print("📤 Will export in ALL formats")
        elif args.export_format:
            print(f"📤 Will export in {args.export_format.upper()} format")
