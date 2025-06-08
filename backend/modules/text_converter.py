import re
import json
from pathlib import Path
from typing import Optional, Union
import black
from schemas import PromptData, ResponseData

from modules.base import ModuleBase


class TextConverter(ModuleBase):

    def applies_before(self) -> bool:
        return False

    def applies_after(self) -> bool:
        return True

    def process_prompt(self, prompt_data: PromptData) -> PromptData:
        return prompt_data

    def process_response(
        self, response_data: ResponseData, prompt_data: PromptData
    ) -> ResponseData:
        model_id = prompt_data.model.id
        safe_model_id = model_id.replace(":", "_")
        output_filename = f"{safe_model_id}.py"
        # Change output_dir to backend/extracted
        output_dir = Path(__file__).parent.parent / "extracted"
        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / output_filename

        # get responce from response_data -> this is setting
        raw_markdown = response_data.output.markdown or ""
        cleaned_code = clean_response_text(raw_markdown)
        response_data.output.code = cleaned_code
        write_cleaned_python_code_to_file(cleaned_code, output_path)
        return response_data


def clean_response_text(response_text: str) -> str:
    """
    Extracts and cleans all Python code blocks from the input text,
    removing markdown code block markers and trailing explanations.
    Concatenates all code blocks into a single string.
    Formats the result using Black.
    """
    if not response_text or not response_text.strip():
        return "no response"

    # Find all code blocks marked with ```python ... ```
    code_blocks = re.findall(
        r"```python(.*?)```", response_text, flags=re.DOTALL | re.IGNORECASE
    )

    # If no python code blocks found, try generic code blocks
    if not code_blocks:
        code_blocks = re.findall(
            r"```(.*?)```", response_text, flags=re.DOTALL | re.IGNORECASE
        )

    # If still no code blocks, treat the whole text as a single block
    if not code_blocks:
        code_blocks = [response_text]

    cleaned_blocks = []
    for block in code_blocks:
        # Remove leading/trailing whitespace and empty lines
        cleaned_block = "\n".join(
            line.rstrip()
            for line in block.strip().splitlines()
            if line.strip()
        )
        cleaned_blocks.append(cleaned_block)

    code = "\n\n".join(filter(None, cleaned_blocks))

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
