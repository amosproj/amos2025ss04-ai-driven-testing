import re
import json
from pathlib import Path
from typing import Optional, Union
import black
from schemas import PromptData, ResponseData

from modules.base import ModuleBase


class TextConverter(ModuleBase):
    """Extrahiert und bereinigt Python-Code aus Markdown-Antworten und formatiert ihn mit Black."""

    order_before = 1
    order_after = 1

    def applies_before(self) -> bool:
        return True

    def applies_after(self) -> bool:
        return True

    def process_prompt(self, prompt_data: PromptData) -> PromptData:
        model_id = prompt_data.model.id
        safe_model_id = model_id.replace(":", "_")

        # Prepare output directory
        output_dir = Path(__file__).parent.parent / "extracted"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Filter and clean the prompt code
        raw_code = prompt_data.input.source_code or ""
        cleaned_code = clean_response_text(raw_code)

        # 1. Save to generic path (used by executor)
        main_output_path = output_dir / "prompt.py"
        with open(main_output_path, "w", encoding="utf-8") as f:
            f.write(cleaned_code)

        # 2. Save to versioned archive path
        archive_output_path = output_dir / f"prompt_{safe_model_id}.py"
        with open(archive_output_path, "w", encoding="utf-8") as f:
            f.write(cleaned_code)

        # Update the prompt data path (used later for execution)
        prompt_data.prompt_code_path = str(main_output_path)
        return prompt_data

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        model_id = prompt_data.model.id
        safe_model_id = model_id.replace(":", "_")

        # Base directory for all outputs
        output_dir = Path(__file__).parent.parent / "extracted"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Clean response code and prepend import line
        raw_markdown = response_data.output.markdown or ""
        import_line = (
            "import sys\n"
            "from pathlib import Path\n"
            "sys.path.insert(0, '/code/extracted')  # Add extracted dir to import path\n"
            "from prompt import *  # Import functions from prompt.py\n\n"
        )
        cleaned_code = import_line + clean_response_text(raw_markdown)

        # 1. Save to generic path (used by executor)
        main_output_path = output_dir / "response.py"
        with open(main_output_path, "w", encoding="utf-8") as f:
            f.write(cleaned_code)

        # 2. Save to versioned archive path
        archive_output_path = output_dir / f"response_{safe_model_id}.py"
        with open(archive_output_path, "w", encoding="utf-8") as f:
            f.write(cleaned_code)

        # Update response_data with both paths
        response_data.output.code = cleaned_code
        response_data.output.output_code_path = str(main_output_path)

        return response_data


def clean_response_text(response_text: str) -> str:
    """
    Extracts and cleans all Python code blocks from the input text,
    removing markdown code block markers and any text before the first code block.
    Handles missing closing code block by extracting everything after the opening marker.
    Formats the result using Black.
    """
    if not response_text or not response_text.strip():
        return "no response"

    # Remove everything before the first code block (```python or ```)
    code_block_start = re.search(
        r"```python", response_text, flags=re.IGNORECASE
    )
    if code_block_start:
        # If there is a closing ```, extract between them; otherwise, take everything after the opening marker
        after_start = response_text[code_block_start.end() :]
        code_block_end = re.search(r"```", after_start)
        if code_block_end:
            code = after_start[: code_block_end.start()].strip()
        else:
            code = after_start.strip()
    else:
        # Fallback: try generic code block
        code_block_start = re.search(r"```", response_text)
        if code_block_start:
            after_start = response_text[code_block_start.end() :]
            code_block_end = re.search(r"```", after_start)
            if code_block_end:
                code = after_start[: code_block_end.start()].strip()
            else:
                code = after_start.strip()
        else:
            code = response_text.strip()

    # Remove leading/trailing empty lines
    code = "\n".join(
        line.rstrip()
        for line in code.splitlines()
        if line.strip() or line == ""
    )

    # Format the code using Black
    try:
        formatted_code = black.format_str(code, mode=black.Mode())
    except Exception:
        formatted_code = fix_indent(code)
        formatted_code = add_pass_to_empty_functions(formatted_code)
        try:
            formatted_code = black.format_str(
                formatted_code, mode=black.Mode()
            )
        except Exception:
            formatted_code = (
                formatted_code  # fallback to fixed code if Black fails again
            )

    return formatted_code


def convert_to_python_file(
    input_path: Union[str, Path],
    destination: Optional[Union[str, Path]] = None,
) -> Path:
    """
    Converts a JSON or Markdown file to a Python file and saves it in the destination directory.
    If destination is not provided, saves to /backend/extracted with the same name as the input file.
    Returns the path to the generated Python file.
    """
    input_path = Path(input_path)
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    if input_path.suffix == ".json":
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        code = clean_response_text(data.get("code", ""))
    elif input_path.suffix in [".md", ".markdown"]:
        with open(input_path, "r", encoding="utf-8") as f:
            text = f.read()
        code = clean_response_text(text)
    else:
        raise ValueError(f"Unsupported file type: {input_path.suffix}")

    output_filename = input_path.stem + ".py"
    if destination is not None:
        output_path = Path(destination) / output_filename
        output_path.parent.mkdir(parents=True, exist_ok=True)
        return write_cleaned_python_code_to_file(code, output_path.name)
    else:
        # Change default output directory to backend/extracted
        output_dir = Path(__file__).parent.parent / "extracted"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / output_filename
        return write_cleaned_python_code_to_file(code, output_path)


def write_cleaned_python_code_to_file(
    text: str, destination_path: Path
) -> Path:
    """
    Cleans the input text to extract Python code blocks and writes the result
    to the specified destination_path. Returns the path to the generated file.
    """
    code = clean_response_text(text)
    # Ensure the parent directory exists
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    with open(destination_path, "w", encoding="utf-8") as f:
        f.write(code)
    return destination_path


def fix_indent(code: str) -> str:
    # Try to fix indentation for class methods with 'self'
    lines = code.splitlines()
    new_lines = []
    inside_class = False
    indent = "    "
    i = 0
    while i < len(lines):
        line = lines[i]
        class_match = re.match(r"^class\s+\w+", line)
        func_match = re.match(r"^def\s+\w+\s*\(.*self.*\):", line)
        if class_match:
            inside_class = True
            new_lines.append(line)
            i += 1
            continue
        if inside_class:
            if func_match:
                # Indent the function definition
                new_lines.append(indent + line)
                i += 1
                # Indent following lines until next def/class at base level
                while i < len(lines):
                    next_line = lines[i]
                    if re.match(
                        r"^(class|def)\s", next_line
                    ) and not next_line.startswith(indent):
                        break
                    if next_line.strip() == "":
                        new_lines.append("")
                    else:
                        new_lines.append(indent + next_line)
                    i += 1
                continue  # skip increment, already done
            # If line is not a function, just add it
            if not line.strip().startswith("def "):
                new_lines.append(line)
        else:
            new_lines.append(line)
        i += 1
    fixed_code = "\n".join(new_lines)
    return fixed_code


def add_pass_to_empty_functions(code_str):
    # This regex matches function definitions that are empty or only contain comments/whitespace
    pattern = re.compile(
        r"(^def\s+\w+\s*\(.*?\):\s*\n"  # function header
        r"(?:(?:\s*#.*\n|\s*\n)*)"
        r")(?=(\s*def|\s*class|\Z))",  # next def/class or end of string
        re.MULTILINE,
    )

    def replacer(match):
        func_header = match.group(1)
        return func_header + "    pass\n"

    # Also handle one-line empty functions: def foo():
    code_str = re.sub(
        r"(^def\s+\w+\s*\(.*?\):\s*)($|\n(?=\s*def|\s*class|\Z))",
        r"\1\n    pass\n",
        code_str,
        flags=re.MULTILINE,
    )
    return pattern.sub(replacer, code_str)
