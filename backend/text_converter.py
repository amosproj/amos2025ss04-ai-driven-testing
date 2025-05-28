import re
import json
import sys
from pathlib import Path
from typing import Optional, Union


def clean_response_text(response_text: str) -> str:
    """
    Extracts and cleans all Python code blocks from the input text,
    removing markdown code block markers and trailing explanations.
    Concatenates all code blocks into a single string.
    """
    if not response_text or not response_text.strip():
        return ""

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

    return "\n\n".join(filter(None, cleaned_blocks))


def convert_to_python_file(
    input_path: Union[str, Path],
    destination: Optional[Union[str, Path]] = None,
) -> Path:
    """
    Converts a JSON or Markdown file to a Python file and saves it in the destination directory.
    If destination is not provided, saves to /backend/outputs/extracted with the same name as the input file.
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
        return write_cleaned_python_code_to_file(code, output_filename)


def write_cleaned_python_code_to_file(
    text: str, destination_file: str
) -> Path:
    """
    Cleans the input text to extract Python code blocks and writes the result
    to outputs/extracted/<destination_file>. Returns the path to the generated file.
    """
    output_dir = Path(__file__).parent / "outputs/extracted"
    output_dir.mkdir(parents=True, exist_ok=True)
    code = clean_response_text(text)
    output_path = output_dir / destination_file
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(code)
    return output_path


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python text_converter.py <input_path> [destination]")
        sys.exit(1)
    input_path = sys.argv[1]
    destination = sys.argv[2] if len(sys.argv) > 2 else None
    try:
        output_path = convert_to_python_file(input_path, destination)
        print(f"Python file generated at: {output_path}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
